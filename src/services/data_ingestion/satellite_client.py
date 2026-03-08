"""
Satellite data client for Sentinel Hub integration
"""
import logging
from datetime import datetime, timedelta

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config.settings import settings

logger = logging.getLogger(__name__)


class SatelliteClient:
    """Client for fetching satellite imagery from Sentinel Hub"""

    def __init__(self):
        self.client_id = settings.sentinel_hub_client_id
        self.client_secret = settings.sentinel_hub_client_secret
        self.base_url = "https://services.sentinel-hub.com"
        self.token: str | None = None
        self.token_expires: datetime | None = None

    async def _get_access_token(self) -> str:
        """Get OAuth access token"""
        if self.token and self.token_expires and datetime.utcnow() < self.token_expires:
            return self.token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/oauth/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }
            )
            response.raise_for_status()
            data = response.json()

            self.token = data["access_token"]
            # Token expires in seconds, refresh 5 minutes before
            expires_in = data.get("expires_in", 3600)
            self.token_expires = datetime.utcnow() + timedelta(seconds=expires_in - 300)

            logger.info("Obtained new Sentinel Hub access token")
            return self.token

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_tile(
        self,
        bbox: tuple[float, float, float, float],
        date_from: datetime,
        date_to: datetime,
        width: int = 512,
        height: int = 512,
    ) -> dict:
        """
        Fetch satellite tile for given bounding box and date range

        Args:
            bbox: Bounding box (min_lon, min_lat, max_lon, max_lat)
            date_from: Start date
            date_to: End date
            width: Image width in pixels
            height: Image height in pixels

        Returns:
            Dictionary with tile data and metadata
        """
        token = await self._get_access_token()

        # Request NDVI, moisture, and RGB bands
        evalscript = """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B04", "B08", "B11"],
                    units: "REFLECTANCE"
                }],
                output: {
                    bands: 3,
                    sampleType: "FLOAT32"
                }
            };
        }

        function evaluatePixel(sample) {
            // NDVI = (NIR - Red) / (NIR + Red)
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04 + 0.0001);

            // Moisture index using SWIR
            let moisture = sample.B11;

            // Red band for visualization
            let red = sample.B04;

            return [ndvi, moisture, red];
        }
        """

        request_body = {
            "input": {
                "bounds": {
                    "bbox": list(bbox),
                    "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": date_from.isoformat() + "Z",
                            "to": date_to.isoformat() + "Z"
                        },
                        "maxCloudCoverage": 30
                    }
                }]
            },
            "output": {
                "width": width,
                "height": height,
                "responses": [{
                    "identifier": "default",
                    "format": {"type": "image/tiff"}
                }]
            },
            "evalscript": evalscript
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/process",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=request_body
            )
            response.raise_for_status()

            logger.info(f"Fetched satellite tile for bbox {bbox}")

            return {
                "data": response.content,
                "bbox": bbox,
                "date_from": date_from,
                "date_to": date_to,
                "width": width,
                "height": height,
                "timestamp": datetime.utcnow()
            }

    async def fetch_tiles_for_region(
        self,
        region_bbox: tuple[float, float, float, float],
        date_from: datetime,
        date_to: datetime,
        tile_size: float = 0.01  # ~1km at equator
    ) -> list[dict]:
        """
        Fetch multiple tiles covering a region

        Args:
            region_bbox: Region bounding box (min_lon, min_lat, max_lon, max_lat)
            date_from: Start date
            date_to: End date
            tile_size: Size of each tile in degrees

        Returns:
            List of tile data dictionaries
        """
        min_lon, min_lat, max_lon, max_lat = region_bbox

        tiles = []
        current_lat = min_lat

        while current_lat < max_lat:
            current_lon = min_lon

            while current_lon < max_lon:
                tile_bbox = (
                    current_lon,
                    current_lat,
                    min(current_lon + tile_size, max_lon),
                    min(current_lat + tile_size, max_lat)
                )

                try:
                    tile_data = await self.fetch_tile(
                        bbox=tile_bbox,
                        date_from=date_from,
                        date_to=date_to
                    )
                    tiles.append(tile_data)
                except Exception as e:
                    logger.error(f"Failed to fetch tile {tile_bbox}: {e}")

                current_lon += tile_size

            current_lat += tile_size

        logger.info(f"Fetched {len(tiles)} tiles for region {region_bbox}")
        return tiles
