"""
Storage manager for satellite tiles and data
"""
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
import hashlib
import boto3
from botocore.exceptions import ClientError

from src.config.settings import settings

logger = logging.getLogger(__name__)


class StorageManager:
    """Manager for storing satellite tiles and data in S3"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
        self.satellite_bucket = settings.s3_bucket_satellite
        self.audio_bucket = settings.s3_bucket_audio
    
    def _generate_tile_key(
        self,
        bbox: tuple,
        date_from: datetime,
        date_to: datetime
    ) -> str:
        """Generate unique S3 key for tile"""
        # Create hash from bbox and dates
        key_string = f"{bbox}_{date_from.isoformat()}_{date_to.isoformat()}"
        hash_value = hashlib.md5(key_string.encode()).hexdigest()
        
        # Organize by date
        date_path = date_from.strftime("%Y/%m/%d")
        
        return f"tiles/{date_path}/{hash_value}.tiff"
    
    async def store_satellite_tile(
        self,
        tile_data: bytes,
        bbox: tuple,
        date_from: datetime,
        date_to: datetime,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Store satellite tile in S3
        
        Args:
            tile_data: Raw tile data
            bbox: Bounding box
            date_from: Start date
            date_to: End date
            metadata: Additional metadata
        
        Returns:
            S3 key of stored tile
        """
        key = self._generate_tile_key(bbox, date_from, date_to)
        
        # Prepare metadata
        s3_metadata = {
            "bbox": str(bbox),
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "stored_at": datetime.utcnow().isoformat()
        }
        if metadata:
            s3_metadata.update({k: str(v) for k, v in metadata.items()})
        
        try:
            self.s3_client.put_object(
                Bucket=self.satellite_bucket,
                Key=key,
                Body=tile_data,
                ContentType='image/tiff',
                Metadata=s3_metadata
            )
            logger.info(f"Stored satellite tile: {key}")
            return key
        except ClientError as e:
            logger.error(f"Failed to store tile {key}: {e}")
            raise
    
    async def retrieve_satellite_tile(self, key: str) -> Optional[bytes]:
        """
        Retrieve satellite tile from S3
        
        Args:
            key: S3 key
        
        Returns:
            Tile data or None if not found
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.satellite_bucket,
                Key=key
            )
            logger.info(f"Retrieved satellite tile: {key}")
            return response['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.warning(f"Tile not found: {key}")
                return None
            logger.error(f"Failed to retrieve tile {key}: {e}")
            raise
    
    async def tile_exists(self, key: str) -> bool:
        """Check if tile exists in S3"""
        try:
            self.s3_client.head_object(
                Bucket=self.satellite_bucket,
                Key=key
            )
            return True
        except ClientError:
            return False
    
    async def store_audio(
        self,
        audio_data: bytes,
        farmer_id: str,
        call_id: str,
        audio_type: str = "advisory"
    ) -> str:
        """
        Store audio file in S3
        
        Args:
            audio_data: Raw audio data
            farmer_id: Farmer ID
            call_id: Call ID
            audio_type: Type of audio (advisory, recording, etc.)
        
        Returns:
            S3 key of stored audio
        """
        timestamp = datetime.utcnow()
        date_path = timestamp.strftime("%Y/%m/%d")
        key = f"audio/{audio_type}/{date_path}/{farmer_id}/{call_id}.mp3"
        
        try:
            self.s3_client.put_object(
                Bucket=self.audio_bucket,
                Key=key,
                Body=audio_data,
                ContentType='audio/mpeg',
                Metadata={
                    "farmer_id": farmer_id,
                    "call_id": call_id,
                    "audio_type": audio_type,
                    "stored_at": timestamp.isoformat()
                }
            )
            logger.info(f"Stored audio: {key}")
            return key
        except ClientError as e:
            logger.error(f"Failed to store audio {key}: {e}")
            raise
    
    async def retrieve_audio(self, key: str) -> Optional[bytes]:
        """Retrieve audio file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.audio_bucket,
                Key=key
            )
            logger.info(f"Retrieved audio: {key}")
            return response['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.warning(f"Audio not found: {key}")
                return None
            logger.error(f"Failed to retrieve audio {key}: {e}")
            raise
    
    async def delete_old_tiles(self, days: int = 365) -> int:
        """
        Delete tiles older than specified days
        
        Args:
            days: Age threshold in days
        
        Returns:
            Number of tiles deleted
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted_count = 0
        
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(
                Bucket=self.satellite_bucket,
                Prefix='tiles/'
            )
            
            for page in pages:
                for obj in page.get('Contents', []):
                    if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                        self.s3_client.delete_object(
                            Bucket=self.satellite_bucket,
                            Key=obj['Key']
                        )
                        deleted_count += 1
            
            logger.info(f"Deleted {deleted_count} old tiles")
            return deleted_count
        except ClientError as e:
            logger.error(f"Failed to delete old tiles: {e}")
            raise
