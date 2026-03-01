"""
Kafka producer for data ingestion events
"""
import logging
import json
from typing import Dict, Any
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

from src.config.settings import settings

logger = logging.getLogger(__name__)


class DataEventProducer:
    """Producer for publishing data ingestion events to Kafka"""
    
    # Topic names
    TOPIC_SATELLITE_DATA = "satellite-data"
    TOPIC_WEATHER_DATA = "weather-data"
    TOPIC_CROP_INDICATORS = "crop-indicators"
    TOPIC_STRESS_ALERTS = "stress-alerts"
    TOPIC_NOTIFICATIONS = "notifications"
    
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers.split(','),
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1,  # Ensure ordering
        )
        logger.info("Kafka producer initialized")
    
    def _add_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add common metadata to event"""
        return {
            **data,
            "event_timestamp": datetime.utcnow().isoformat(),
            "producer": "data-ingestion-service"
        }
    
    async def publish_satellite_data_event(
        self,
        tile_key: str,
        bbox: tuple,
        date_from: datetime,
        date_to: datetime
    ) -> None:
        """
        Publish satellite data ingestion event
        
        Args:
            tile_key: S3 key of stored tile
            bbox: Bounding box
            date_from: Start date
            date_to: End date
        """
        event = self._add_metadata({
            "event_type": "satellite_tile_ingested",
            "tile_key": tile_key,
            "bbox": bbox,
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat()
        })
        
        try:
            future = self.producer.send(
                self.TOPIC_SATELLITE_DATA,
                key=tile_key,
                value=event
            )
            # Wait for send to complete
            future.get(timeout=10)
            logger.info(f"Published satellite data event for {tile_key}")
        except KafkaError as e:
            logger.error(f"Failed to publish satellite data event: {e}")
            raise
    
    async def publish_weather_data_event(
        self,
        location: Dict[str, float],
        weather_data: Dict[str, Any],
        data_type: str = "current"
    ) -> None:
        """
        Publish weather data ingestion event
        
        Args:
            location: Location dict with lat/lon
            weather_data: Weather data
            data_type: Type of weather data (current, forecast, historical)
        """
        event = self._add_metadata({
            "event_type": "weather_data_ingested",
            "location": location,
            "data_type": data_type,
            "weather_data": weather_data
        })
        
        key = f"{location['lat']}_{location['lon']}"
        
        try:
            future = self.producer.send(
                self.TOPIC_WEATHER_DATA,
                key=key,
                value=event
            )
            future.get(timeout=10)
            logger.info(f"Published weather data event for {location}")
        except KafkaError as e:
            logger.error(f"Failed to publish weather data event: {e}")
            raise
    
    async def publish_crop_indicator_event(
        self,
        plot_id: str,
        indicators: Dict[str, Any]
    ) -> None:
        """
        Publish crop health indicator event
        
        Args:
            plot_id: Farm plot ID
            indicators: Crop health indicators
        """
        event = self._add_metadata({
            "event_type": "crop_indicators_calculated",
            "plot_id": plot_id,
            "indicators": indicators
        })
        
        try:
            future = self.producer.send(
                self.TOPIC_CROP_INDICATORS,
                key=plot_id,
                value=event
            )
            future.get(timeout=10)
            logger.info(f"Published crop indicator event for plot {plot_id}")
        except KafkaError as e:
            logger.error(f"Failed to publish crop indicator event: {e}")
            raise
    
    async def publish_stress_alert_event(
        self,
        farmer_id: str,
        plot_id: str,
        alert_data: Dict[str, Any]
    ) -> None:
        """
        Publish stress alert event
        
        Args:
            farmer_id: Farmer ID
            plot_id: Farm plot ID
            alert_data: Alert data including risk score, stress type, etc.
        """
        event = self._add_metadata({
            "event_type": "stress_alert_triggered",
            "farmer_id": farmer_id,
            "plot_id": plot_id,
            "alert_data": alert_data
        })
        
        try:
            future = self.producer.send(
                self.TOPIC_STRESS_ALERTS,
                key=farmer_id,
                value=event
            )
            future.get(timeout=10)
            logger.info(f"Published stress alert for farmer {farmer_id}, plot {plot_id}")
        except KafkaError as e:
            logger.error(f"Failed to publish stress alert event: {e}")
            raise
    
    async def publish_notification_event(
        self,
        farmer_id: str,
        notification_type: str,
        notification_data: Dict[str, Any]
    ) -> None:
        """
        Publish notification event
        
        Args:
            farmer_id: Farmer ID
            notification_type: Type of notification (call, sms, etc.)
            notification_data: Notification data
        """
        event = self._add_metadata({
            "event_type": "notification_scheduled",
            "farmer_id": farmer_id,
            "notification_type": notification_type,
            "notification_data": notification_data
        })
        
        try:
            future = self.producer.send(
                self.TOPIC_NOTIFICATIONS,
                key=farmer_id,
                value=event
            )
            future.get(timeout=10)
            logger.info(f"Published notification event for farmer {farmer_id}")
        except KafkaError as e:
            logger.error(f"Failed to publish notification event: {e}")
            raise
    
    def close(self):
        """Close producer and flush pending messages"""
        self.producer.flush()
        self.producer.close()
        logger.info("Kafka producer closed")
