"""
Weather data analyzer for trend analysis and risk assessment
"""
import logging
from datetime import datetime, timedelta

import numpy as np

logger = logging.getLogger(__name__)


class WeatherAnalyzer:
    """Analyzer for weather data trends and risk assessment"""

    # Risk thresholds
    TEMP_HIGH_THRESHOLD = 40  # °C
    TEMP_LOW_THRESHOLD = 5    # °C
    HUMIDITY_LOW_THRESHOLD = 30  # %
    WIND_HIGH_THRESHOLD = 50  # km/h
    RAIN_HEAVY_THRESHOLD = 50  # mm/day

    @staticmethod
    def calculate_temperature_trend(
        weather_history: list[dict]
    ) -> dict[str, float]:
        """
        Calculate temperature trends from historical data

        Args:
            weather_history: List of weather data dictionaries

        Returns:
            Dictionary with trend statistics
        """
        if not weather_history:
            return {"trend": 0.0, "mean": 0.0, "std": 0.0}

        temps = [w["temperature"] for w in weather_history]

        # Calculate linear trend
        x = np.arange(len(temps))
        coeffs = np.polyfit(x, temps, 1)
        trend = coeffs[0]  # Slope

        return {
            "trend": float(trend),
            "mean": float(np.mean(temps)),
            "std": float(np.std(temps)),
            "min": float(np.min(temps)),
            "max": float(np.max(temps))
        }

    @staticmethod
    def calculate_rainfall_accumulation(
        weather_history: list[dict],
        days: int = 7
    ) -> float:
        """
        Calculate accumulated rainfall over period

        Args:
            weather_history: List of weather data
            days: Number of days to accumulate

        Returns:
            Total rainfall in mm
        """
        cutoff = datetime.utcnow() - timedelta(days=days)

        total_rain = 0.0
        for weather in weather_history:
            if weather.get("timestamp") and weather["timestamp"] > cutoff:
                total_rain += weather.get("rain_1h", 0) + weather.get("rain_3h", 0)

        return total_rain

    @staticmethod
    def assess_heat_stress_risk(
        current_temp: float,
        humidity: float,
        forecast: list[dict]
    ) -> dict[str, any]:
        """
        Assess heat stress risk for crops

        Args:
            current_temp: Current temperature
            humidity: Current humidity
            forecast: Weather forecast

        Returns:
            Risk assessment dictionary
        """
        # Calculate heat index
        heat_index = WeatherAnalyzer._calculate_heat_index(current_temp, humidity)

        # Check forecast for sustained high temperatures
        high_temp_days = 0
        for day in forecast[:7]:  # Next 7 days
            if day.get("temp_max", 0) > WeatherAnalyzer.TEMP_HIGH_THRESHOLD:
                high_temp_days += 1

        # Determine risk level
        if heat_index > 45 or high_temp_days >= 3:
            risk_level = "high"
            description = "Severe heat stress risk"
        elif heat_index > 40 or high_temp_days >= 2:
            risk_level = "medium"
            description = "Moderate heat stress risk"
        elif heat_index > 35 or high_temp_days >= 1:
            risk_level = "low"
            description = "Low heat stress risk"
        else:
            risk_level = "none"
            description = "No heat stress risk"

        return {
            "risk_level": risk_level,
            "description": description,
            "heat_index": heat_index,
            "high_temp_days_forecast": high_temp_days,
            "current_temp": current_temp,
            "humidity": humidity
        }

    @staticmethod
    def assess_drought_risk(
        rainfall_7day: float,
        rainfall_30day: float,
        humidity: float,
        forecast: list[dict]
    ) -> dict[str, any]:
        """
        Assess drought risk

        Args:
            rainfall_7day: 7-day accumulated rainfall
            rainfall_30day: 30-day accumulated rainfall
            humidity: Current humidity
            forecast: Weather forecast

        Returns:
            Risk assessment dictionary
        """
        # Check forecast for rain
        rain_forecast_days = 0
        for day in forecast[:7]:
            if day.get("pop", 0) > 0.3:  # Probability of precipitation > 30%
                rain_forecast_days += 1

        # Determine risk level
        if rainfall_7day < 5 and rainfall_30day < 20 and rain_forecast_days == 0:
            risk_level = "high"
            description = "Severe drought risk"
        elif rainfall_7day < 10 and rainfall_30day < 40 and rain_forecast_days <= 1:
            risk_level = "medium"
            description = "Moderate drought risk"
        elif rainfall_7day < 20 and rainfall_30day < 60:
            risk_level = "low"
            description = "Low drought risk"
        else:
            risk_level = "none"
            description = "No drought risk"

        return {
            "risk_level": risk_level,
            "description": description,
            "rainfall_7day": rainfall_7day,
            "rainfall_30day": rainfall_30day,
            "humidity": humidity,
            "rain_forecast_days": rain_forecast_days
        }

    @staticmethod
    def assess_frost_risk(
        current_temp: float,
        forecast: list[dict]
    ) -> dict[str, any]:
        """
        Assess frost risk

        Args:
            current_temp: Current temperature
            forecast: Weather forecast

        Returns:
            Risk assessment dictionary
        """
        # Check forecast for low temperatures
        frost_risk_days = []
        for i, day in enumerate(forecast[:7]):
            temp_min = day.get("temp_min", current_temp)
            if temp_min < WeatherAnalyzer.TEMP_LOW_THRESHOLD:
                frost_risk_days.append(i)

        if len(frost_risk_days) > 0:
            if frost_risk_days[0] == 0:  # Today
                risk_level = "high"
                description = "Immediate frost risk"
            elif frost_risk_days[0] <= 2:  # Within 2 days
                risk_level = "medium"
                description = "Frost risk in next 2 days"
            else:
                risk_level = "low"
                description = "Frost risk later this week"
        else:
            risk_level = "none"
            description = "No frost risk"

        return {
            "risk_level": risk_level,
            "description": description,
            "current_temp": current_temp,
            "frost_risk_days": frost_risk_days
        }

    @staticmethod
    def assess_wind_damage_risk(
        wind_speed: float,
        forecast: list[dict]
    ) -> dict[str, any]:
        """
        Assess wind damage risk

        Args:
            wind_speed: Current wind speed (km/h)
            forecast: Weather forecast

        Returns:
            Risk assessment dictionary
        """
        # Check forecast for high winds
        high_wind_days = 0
        max_wind_forecast = wind_speed

        for day in forecast[:3]:  # Next 3 days
            day_wind = day.get("wind_speed", 0) * 3.6  # Convert m/s to km/h
            if day_wind > WeatherAnalyzer.WIND_HIGH_THRESHOLD:
                high_wind_days += 1
            max_wind_forecast = max(max_wind_forecast, day_wind)

        if max_wind_forecast > 70 or high_wind_days >= 2:
            risk_level = "high"
            description = "Severe wind damage risk"
        elif max_wind_forecast > 60 or high_wind_days >= 1:
            risk_level = "medium"
            description = "Moderate wind damage risk"
        elif max_wind_forecast > 50:
            risk_level = "low"
            description = "Low wind damage risk"
        else:
            risk_level = "none"
            description = "No wind damage risk"

        return {
            "risk_level": risk_level,
            "description": description,
            "current_wind_speed": wind_speed,
            "max_wind_forecast": max_wind_forecast,
            "high_wind_days": high_wind_days
        }

    @staticmethod
    def _calculate_heat_index(temp: float, humidity: float) -> float:
        """
        Calculate heat index (feels like temperature)

        Args:
            temp: Temperature in Celsius
            humidity: Relative humidity (0-100)

        Returns:
            Heat index in Celsius
        """
        # Simplified heat index formula
        if temp < 27:
            return temp

        # Convert to Fahrenheit for calculation
        T = temp * 9/5 + 32
        RH = humidity

        HI = -42.379 + 2.04901523*T + 10.14333127*RH - 0.22475541*T*RH
        HI += -0.00683783*T*T - 0.05481717*RH*RH + 0.00122874*T*T*RH
        HI += 0.00085282*T*RH*RH - 0.00000199*T*T*RH*RH

        # Convert back to Celsius
        return (HI - 32) * 5/9

    def analyze_weather_risks(
        self,
        current_weather: dict,
        forecast: list[dict],
        weather_history: list[dict]
    ) -> dict[str, any]:
        """
        Comprehensive weather risk analysis

        Args:
            current_weather: Current weather data
            forecast: Weather forecast
            weather_history: Historical weather data

        Returns:
            Comprehensive risk assessment
        """
        # Calculate rainfall accumulations
        rainfall_7day = self.calculate_rainfall_accumulation(weather_history, days=7)
        rainfall_30day = self.calculate_rainfall_accumulation(weather_history, days=30)

        # Assess all risk types
        heat_risk = self.assess_heat_stress_risk(
            current_weather["temperature"],
            current_weather["humidity"],
            forecast
        )

        drought_risk = self.assess_drought_risk(
            rainfall_7day,
            rainfall_30day,
            current_weather["humidity"],
            forecast
        )

        frost_risk = self.assess_frost_risk(
            current_weather["temperature"],
            forecast
        )

        wind_risk = self.assess_wind_damage_risk(
            current_weather["wind_speed"],
            forecast
        )

        # Determine overall risk level
        risk_levels = [
            heat_risk["risk_level"],
            drought_risk["risk_level"],
            frost_risk["risk_level"],
            wind_risk["risk_level"]
        ]

        if "high" in risk_levels:
            overall_risk = "high"
        elif "medium" in risk_levels:
            overall_risk = "medium"
        elif "low" in risk_levels:
            overall_risk = "low"
        else:
            overall_risk = "none"

        result = {
            "overall_risk": overall_risk,
            "heat_stress": heat_risk,
            "drought": drought_risk,
            "frost": frost_risk,
            "wind_damage": wind_risk,
            "rainfall_7day": rainfall_7day,
            "rainfall_30day": rainfall_30day,
            "analyzed_at": datetime.utcnow().isoformat()
        }

        logger.info(f"Weather risk analysis complete: overall_risk={overall_risk}")

        return result
