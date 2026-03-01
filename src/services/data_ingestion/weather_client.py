"""
Weather data client for OpenWeatherMap integration
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config.settings import settings

logger = logging.getLogger(__name__)


class WeatherClient:
    """Client for fetching weather data from OpenWeatherMap"""
    
    def __init__(self):
        self.api_key = settings.openweathermap_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_current_weather(
        self,
        lat: float,
        lon: float
    ) -> Dict:
        """
        Fetch current weather for location
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            Weather data dictionary
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Fetched current weather for ({lat}, {lon})")
            
            return {
                "location": {"lat": lat, "lon": lon},
                "timestamp": datetime.utcnow(),
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg"),
                "clouds": data["clouds"]["all"],
                "weather": data["weather"][0]["main"],
                "weather_description": data["weather"][0]["description"],
                "rain_1h": data.get("rain", {}).get("1h", 0),
                "rain_3h": data.get("rain", {}).get("3h", 0),
            }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_forecast(
        self,
        lat: float,
        lon: float,
        days: int = 5
    ) -> List[Dict]:
        """
        Fetch weather forecast for location
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days (max 5 for free tier)
        
        Returns:
            List of forecast data dictionaries
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric",
                    "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
                }
            )
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data["list"]:
                forecasts.append({
                    "location": {"lat": lat, "lon": lon},
                    "timestamp": datetime.fromtimestamp(item["dt"]),
                    "temperature": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "temp_min": item["main"]["temp_min"],
                    "temp_max": item["main"]["temp_max"],
                    "humidity": item["main"]["humidity"],
                    "pressure": item["main"]["pressure"],
                    "wind_speed": item["wind"]["speed"],
                    "wind_direction": item["wind"].get("deg"),
                    "clouds": item["clouds"]["all"],
                    "weather": item["weather"][0]["main"],
                    "weather_description": item["weather"][0]["description"],
                    "rain_3h": item.get("rain", {}).get("3h", 0),
                    "pop": item.get("pop", 0),  # Probability of precipitation
                })
            
            logger.info(f"Fetched {len(forecasts)} forecast entries for ({lat}, {lon})")
            return forecasts
    
    async def fetch_historical_weather(
        self,
        lat: float,
        lon: float,
        timestamp: int
    ) -> Dict:
        """
        Fetch historical weather data (requires paid plan)
        
        Args:
            lat: Latitude
            lon: Longitude
            timestamp: Unix timestamp
        
        Returns:
            Historical weather data dictionary
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/onecall/timemachine",
                params={
                    "lat": lat,
                    "lon": lon,
                    "dt": timestamp,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            current = data["current"]
            return {
                "location": {"lat": lat, "lon": lon},
                "timestamp": datetime.fromtimestamp(timestamp),
                "temperature": current["temp"],
                "feels_like": current["feels_like"],
                "humidity": current["humidity"],
                "pressure": current["pressure"],
                "wind_speed": current["wind_speed"],
                "wind_direction": current.get("wind_deg"),
                "clouds": current["clouds"],
                "weather": current["weather"][0]["main"],
                "weather_description": current["weather"][0]["description"],
                "rain_1h": current.get("rain", {}).get("1h", 0),
            }
    
    async def fetch_weather_alerts(
        self,
        lat: float,
        lon: float
    ) -> List[Dict]:
        """
        Fetch weather alerts for location
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            List of weather alerts
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/onecall",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "exclude": "current,minutely,hourly,daily"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            alerts = []
            for alert in data.get("alerts", []):
                alerts.append({
                    "location": {"lat": lat, "lon": lon},
                    "event": alert["event"],
                    "start": datetime.fromtimestamp(alert["start"]),
                    "end": datetime.fromtimestamp(alert["end"]),
                    "sender": alert["sender_name"],
                    "description": alert["description"],
                })
            
            logger.info(f"Fetched {len(alerts)} weather alerts for ({lat}, {lon})")
            return alerts
