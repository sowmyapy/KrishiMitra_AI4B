"""
Automated monitoring service for continuous farmer monitoring
"""
import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.models.advisory import Advisory
from src.models.farmer import Farmer, FarmPlot
from src.services.communication.voice_call_service import VoiceCallService

logger = logging.getLogger(__name__)


class AutoMonitorService:
    """Service for automated farmer monitoring"""

    def __init__(self):
        self.is_running = False
        self.monitor_task = None
        self.check_interval = 3600  # 1 hour in seconds
        self.risk_threshold = 70  # Generate advisory if risk > 70
        self.call_threshold = 60  # LOWERED FOR TESTING: Make call if risk > 60
        self.voice_service = VoiceCallService()
        self.monitoring_stats = {
            "started_at": None,
            "last_check": None,
            "total_checks": 0,  # Number of monitoring cycles
            "farmers_monitored": 0,  # Unique farmers in last check
            "advisories_generated": 0,
            "calls_made": 0,
            "errors": 0
        }

    async def start_monitoring(self):
        """Start the automated monitoring service"""
        if self.is_running:
            logger.warning("Monitoring service is already running")
            return

        self.is_running = True
        self.monitoring_stats["started_at"] = datetime.utcnow().isoformat()
        logger.info("Starting automated monitoring service")

        # Start monitoring loop
        self.monitor_task = asyncio.create_task(self._monitoring_loop())

    async def stop_monitoring(self):
        """Stop the automated monitoring service"""
        if not self.is_running:
            logger.warning("Monitoring service is not running")
            return

        self.is_running = False

        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass

        logger.info("Stopped automated monitoring service")

    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                await self._check_all_farmers()
                self.monitoring_stats["last_check"] = datetime.utcnow().isoformat()

                # Wait for next check
                await asyncio.sleep(self.check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                self.monitoring_stats["errors"] += 1
                await asyncio.sleep(60)  # Wait 1 minute before retry

    async def _check_all_farmers(self):
        """Check all farmers and take action based on risk"""
        db = SessionLocal()
        try:
            # Get all farmers
            farmers = db.query(Farmer).all()
            logger.info(f"Checking {len(farmers)} farmers")

            # Reset farmers_monitored for this check
            farmers_checked = 0

            for farmer in farmers:
                try:
                    await self._check_farmer(farmer, db)
                    farmers_checked += 1
                except Exception as e:
                    logger.error(f"Error checking farmer {farmer.farmer_id}: {e}")
                    self.monitoring_stats["errors"] += 1

            # Update stats
            self.monitoring_stats["farmers_monitored"] = farmers_checked
            self.monitoring_stats["total_checks"] += 1

        finally:
            db.close()

    async def _check_farmer(self, farmer: Farmer, db: Session):
        """Check individual farmer and take action"""
        # Get farmer's plots
        plots = db.query(FarmPlot).filter(FarmPlot.farmer_id == farmer.farmer_id).all()

        if not plots:
            logger.debug(f"No plots for farmer {farmer.farmer_id}")
            return

        # Check if farmer already has a recent advisory (within last 6 hours)
        recent_advisory = db.query(Advisory).filter(
            Advisory.farmer_id == farmer.farmer_id,
            Advisory.created_at >= datetime.utcnow() - timedelta(hours=6)
        ).first()

        if recent_advisory:
            logger.debug(f"Farmer {farmer.farmer_id} has recent advisory, skipping")
            return

        # Calculate risk score (simplified - in production, use actual satellite/weather data)
        risk_score = await self._calculate_risk_score(farmer, plots[0], db)

        logger.info(f"Farmer {farmer.farmer_id} risk score: {risk_score}")

        # Take action based on risk score
        if risk_score >= self.risk_threshold:
            # Generate advisory
            advisory_created = await self._generate_advisory(farmer, db)

            if advisory_created and risk_score >= self.call_threshold:
                # Make voice call for high risk
                await self._make_call(farmer)

    async def _calculate_risk_score(self, farmer: Farmer, plot: FarmPlot, db: Session) -> float:
        """
        Calculate risk score for farmer based on satellite and weather data
        """
        try:
            from src.services.satellite.sentinel_service import SentinelService
            from src.services.weather.weather_service import WeatherService

            sentinel_service = SentinelService()
            weather_service = WeatherService()

            # Get NDVI data
            ndvi_data = await sentinel_service.get_ndvi(
                latitude=plot.latitude,
                longitude=plot.longitude,
                start_date=(datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d"),
                end_date=datetime.utcnow().strftime("%Y-%m-%d")
            )

            ndvi = ndvi_data.get("ndvi", 0.5)

            # Get weather data
            weather_data = await weather_service.get_current_weather(
                latitude=plot.latitude,
                longitude=plot.longitude
            )

            temperature = weather_data.get("temperature", 25)
            humidity = weather_data.get("humidity", 50)

            # Calculate risk score based on NDVI and weather
            risk_score = 50.0  # Base risk

            # NDVI-based risk (lower NDVI = higher risk)
            if ndvi < 0.2:
                risk_score += 40  # Severe stress
            elif ndvi < 0.3:
                risk_score += 30  # High stress
            elif ndvi < 0.4:
                risk_score += 20  # Moderate stress
            elif ndvi < 0.5:
                risk_score += 10  # Mild stress

            # Temperature-based risk
            if temperature > 35:
                risk_score += 15  # Heat stress
            elif temperature > 30:
                risk_score += 10

            # Humidity-based risk
            if humidity < 30:
                risk_score += 10  # Dry conditions
            elif humidity > 80:
                risk_score += 5  # High humidity

            # Cap at 100
            risk_score = min(risk_score, 100.0)

            logger.info(f"Risk score for farmer {farmer.farmer_id}: {risk_score} (NDVI: {ndvi}, Temp: {temperature}, Humidity: {humidity})")

            return risk_score

        except Exception as e:
            logger.error(f"Error calculating risk score: {e}")
            # Return moderate risk as fallback
            return 65.0

    async def _generate_advisory(self, farmer: Farmer, db: Session) -> bool:
        """Generate advisory for farmer"""
        try:
            logger.info(f"Generating advisory for farmer {farmer.farmer_id}")

            # Get farmer's first plot
            plot = db.query(FarmPlot).filter(FarmPlot.farmer_id == farmer.farmer_id).first()
            if not plot:
                logger.warning(f"No plot found for farmer {farmer.farmer_id}")
                return False

            # Import advisory generation logic
            from src.services.advisory.advisory_generator import AdvisoryGenerator
            from src.services.satellite.sentinel_service import SentinelService
            from src.services.weather.weather_service import WeatherService

            # Fetch real data
            sentinel_service = SentinelService()
            weather_service = WeatherService()
            advisory_generator = AdvisoryGenerator()

            # Get satellite data (NDVI)
            ndvi_data = await sentinel_service.get_ndvi(
                latitude=plot.latitude,
                longitude=plot.longitude,
                start_date=(datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d"),
                end_date=datetime.utcnow().strftime("%Y-%m-%d")
            )

            # Get weather data
            weather_data = await weather_service.get_current_weather(
                latitude=plot.latitude,
                longitude=plot.longitude
            )

            # Generate advisory
            advisory_text, stress_type, urgency_level, risk_score, actions = \
                await advisory_generator.generate_advisory(
                    farmer=farmer,
                    plot=plot,
                    ndvi_value=ndvi_data.get("ndvi", 0.5),
                    weather_data=weather_data,
                    language=farmer.preferred_language
                )

            # Create advisory in database
            new_advisory = Advisory(
                farmer_id=farmer.farmer_id,
                farm_plot_id=plot.farm_plot_id,
                advisory_text=advisory_text,
                stress_type=stress_type,
                urgency_level=urgency_level,
                risk_score=risk_score,
                actions=actions,
                expires_at=datetime.utcnow() + timedelta(days=7)
            )

            db.add(new_advisory)
            db.commit()
            db.refresh(new_advisory)

            logger.info(f"Advisory created for farmer {farmer.farmer_id}: {new_advisory.advisory_id}")
            self.monitoring_stats["advisories_generated"] += 1
            return True

        except Exception as e:
            logger.error(f"Failed to generate advisory for {farmer.farmer_id}: {e}", exc_info=True)
            db.rollback()
            return False

    async def _make_call(self, farmer: Farmer):
        """Make voice call to farmer"""
        try:
            import os
            base_url = os.getenv("NGROK_URL", "https://emma-autecologic-gregg.ngrok-free.dev")
            callback_url = f"{base_url}/api/v1/voice/advisory"

            # Initiate call (no calling hours restriction)
            call_result = await self.voice_service.initiate_call(
                to_number=farmer.phone_number,
                callback_url=callback_url,
                farmer_id=str(farmer.farmer_id),
                call_type="advisory"
            )

            logger.info(f"Call initiated for farmer {farmer.farmer_id}: {call_result['call_sid']}")
            self.monitoring_stats["calls_made"] += 1

        except Exception as e:
            logger.error(f"Failed to make call to {farmer.farmer_id}: {e}")

    def get_status(self) -> dict:
        """Get monitoring service status"""
        return {
            "is_running": self.is_running,
            "check_interval_seconds": self.check_interval,
            "risk_threshold": self.risk_threshold,
            "call_threshold": self.call_threshold,
            "stats": self.monitoring_stats
        }

    def update_settings(self, settings: dict):
        """Update monitoring settings"""
        if "check_interval" in settings:
            self.check_interval = settings["check_interval"]

        if "risk_threshold" in settings:
            self.risk_threshold = settings["risk_threshold"]

        if "call_threshold" in settings:
            self.call_threshold = settings["call_threshold"]

        logger.info(f"Updated monitoring settings: {settings}")


# Global instance
auto_monitor_service = AutoMonitorService()
