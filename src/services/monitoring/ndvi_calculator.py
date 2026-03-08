"""
NDVI and vegetation index calculator
"""
import logging
from datetime import datetime

import numpy as np

logger = logging.getLogger(__name__)


class NDVICalculator:
    """Calculator for NDVI and other vegetation indices"""

    @staticmethod
    def calculate_ndvi(nir_band: np.ndarray, red_band: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Vegetation Index (NDVI)

        NDVI = (NIR - Red) / (NIR + Red)
        Range: -1 to 1 (higher values indicate healthier vegetation)

        Args:
            nir_band: Near-infrared band values
            red_band: Red band values

        Returns:
            NDVI values
        """
        if nir_band.shape != red_band.shape:
            raise ValueError("NIR and Red bands must have the same shape")

        # Add small epsilon to avoid division by zero
        ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)

        # Clip to valid range
        ndvi = np.clip(ndvi, -1, 1)

        return ndvi

    @staticmethod
    def calculate_evi(
        nir_band: np.ndarray,
        red_band: np.ndarray,
        blue_band: np.ndarray,
        G: float = 2.5,
        C1: float = 6.0,
        C2: float = 7.5,
        L: float = 1.0
    ) -> np.ndarray:
        """
        Calculate Enhanced Vegetation Index (EVI)

        EVI = G * ((NIR - Red) / (NIR + C1*Red - C2*Blue + L))

        Args:
            nir_band: Near-infrared band
            red_band: Red band
            blue_band: Blue band
            G: Gain factor
            C1, C2: Aerosol resistance coefficients
            L: Canopy background adjustment

        Returns:
            EVI values
        """
        numerator = nir_band - red_band
        denominator = nir_band + C1 * red_band - C2 * blue_band + L + 1e-8

        evi = G * (numerator / denominator)

        return np.clip(evi, -1, 1)

    @staticmethod
    def calculate_savi(
        nir_band: np.ndarray,
        red_band: np.ndarray,
        L: float = 0.5
    ) -> np.ndarray:
        """
        Calculate Soil Adjusted Vegetation Index (SAVI)

        SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)

        Args:
            nir_band: Near-infrared band
            red_band: Red band
            L: Soil brightness correction factor (0.5 for moderate vegetation)

        Returns:
            SAVI values
        """
        numerator = nir_band - red_band
        denominator = nir_band + red_band + L + 1e-8

        savi = (numerator / denominator) * (1 + L)

        return np.clip(savi, -1, 1)

    @staticmethod
    def calculate_moisture_index(swir_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Moisture Index (NDMI)

        NDMI = (NIR - SWIR) / (NIR + SWIR)
        Range: -1 to 1 (higher values indicate more moisture)

        Args:
            swir_band: Short-wave infrared band
            nir_band: Near-infrared band

        Returns:
            NDMI values
        """
        ndmi = (nir_band - swir_band) / (nir_band + swir_band + 1e-8)
        return np.clip(ndmi, -1, 1)

    @staticmethod
    def interpret_ndvi(ndvi_value: float) -> dict[str, str]:
        """
        Interpret NDVI value

        Args:
            ndvi_value: NDVI value

        Returns:
            Dictionary with health status and description
        """
        if ndvi_value < 0:
            return {
                "status": "no_vegetation",
                "description": "Water, snow, or bare soil"
            }
        elif ndvi_value < 0.2:
            return {
                "status": "sparse_vegetation",
                "description": "Sparse or stressed vegetation"
            }
        elif ndvi_value < 0.4:
            return {
                "status": "moderate_vegetation",
                "description": "Moderate vegetation health"
            }
        elif ndvi_value < 0.6:
            return {
                "status": "healthy_vegetation",
                "description": "Healthy vegetation"
            }
        else:
            return {
                "status": "very_healthy_vegetation",
                "description": "Very healthy, dense vegetation"
            }

    @staticmethod
    def calculate_statistics(values: np.ndarray) -> dict[str, float]:
        """
        Calculate statistics for index values

        Args:
            values: Array of index values

        Returns:
            Dictionary with statistics
        """
        # Remove NaN values
        valid_values = values[~np.isnan(values)]

        if len(valid_values) == 0:
            return {
                "mean": 0.0,
                "median": 0.0,
                "std": 0.0,
                "min": 0.0,
                "max": 0.0,
                "percentile_25": 0.0,
                "percentile_75": 0.0
            }

        return {
            "mean": float(np.mean(valid_values)),
            "median": float(np.median(valid_values)),
            "std": float(np.std(valid_values)),
            "min": float(np.min(valid_values)),
            "max": float(np.max(valid_values)),
            "percentile_25": float(np.percentile(valid_values, 25)),
            "percentile_75": float(np.percentile(valid_values, 75))
        }

    @staticmethod
    def detect_anomalies(
        current_ndvi: float,
        historical_mean: float,
        historical_std: float,
        threshold_std: float = 2.0
    ) -> tuple[bool, float]:
        """
        Detect NDVI anomalies using statistical threshold

        Args:
            current_ndvi: Current NDVI value
            historical_mean: Historical mean NDVI
            historical_std: Historical standard deviation
            threshold_std: Number of standard deviations for anomaly

        Returns:
            Tuple of (is_anomaly, z_score)
        """
        if historical_std == 0:
            return False, 0.0

        z_score = (current_ndvi - historical_mean) / historical_std
        is_anomaly = abs(z_score) > threshold_std

        return is_anomaly, z_score

    def process_tile(
        self,
        tile_data: np.ndarray,
        bbox: tuple[float, float, float, float],
        timestamp: datetime
    ) -> dict:
        """
        Process satellite tile and calculate all indices

        Args:
            tile_data: Tile data with shape (height, width, bands)
            bbox: Bounding box
            timestamp: Timestamp of data

        Returns:
            Dictionary with calculated indices and statistics
        """
        # Assuming tile_data has 3 bands: [NDVI, Moisture, Red]
        # (from the evalscript in satellite_client.py)

        if tile_data.shape[2] < 3:
            raise ValueError("Tile data must have at least 3 bands")

        ndvi_band = tile_data[:, :, 0]
        moisture_band = tile_data[:, :, 1]

        # Calculate statistics
        ndvi_stats = self.calculate_statistics(ndvi_band)
        moisture_stats = self.calculate_statistics(moisture_band)

        # Interpret overall health
        health_interpretation = self.interpret_ndvi(ndvi_stats["mean"])

        result = {
            "bbox": bbox,
            "timestamp": timestamp.isoformat(),
            "ndvi": {
                **ndvi_stats,
                "interpretation": health_interpretation
            },
            "moisture": moisture_stats,
            "processed_at": datetime.utcnow().isoformat()
        }

        logger.info(f"Processed tile for bbox {bbox}: NDVI mean={ndvi_stats['mean']:.3f}")

        return result
