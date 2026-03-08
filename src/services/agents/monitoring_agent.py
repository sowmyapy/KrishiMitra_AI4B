"""
Monitoring Agent - Autonomous anomaly detection and investigation
"""
import logging
from datetime import datetime
from typing import Any

from src.services.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class MonitoringAgent(BaseAgent):
    """Agent for monitoring crop health and detecting anomalies"""

    def __init__(self, tools, knowledge_base):
        super().__init__(
            name="Monitoring Agent",
            role="crop health monitoring and anomaly detection",
            tools=tools,
            knowledge_base=knowledge_base
        )

    def _get_responsibilities(self) -> str:
        return """- Monitor NDVI and vegetation indices for anomalies
- Investigate sudden changes in crop health
- Check weather patterns and neighboring farms
- Assess threat level and urgency
- Reduce false positives through contextual analysis
- Decide whether to escalate to diagnostic agent"""

    def think(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Analyze crop health data and detect anomalies

        Args:
            context: Contains ndvi_data, weather_data, historical_data, plot_info

        Returns:
            Decision on whether anomaly is real threat
        """
        ndvi_data = context.get("ndvi_data", {})
        weather_data = context.get("weather_data", {})
        historical_data = context.get("historical_data", {})
        plot_info = context.get("plot_info", {})

        # Step 1: Detect anomaly
        anomaly_detected, z_score = self._detect_anomaly(ndvi_data, historical_data)

        if not anomaly_detected:
            return {
                "anomaly_detected": False,
                "threat_level": "none",
                "action": "continue_monitoring",
                "reasoning": "No significant anomaly detected in NDVI values"
            }

        # Step 2: Investigate context
        investigation = self._investigate_anomaly(
            ndvi_data,
            weather_data,
            historical_data,
            plot_info
        )

        # Step 3: Assess threat
        threat_assessment = self._assess_threat(investigation)

        # Step 4: Make decision
        decision = self._make_decision(threat_assessment, investigation)

        # Log decision
        reasoning = self._build_reasoning(investigation, threat_assessment)
        self.log_decision(decision, context, reasoning)

        return decision

    def _detect_anomaly(
        self,
        ndvi_data: dict,
        historical_data: dict
    ) -> tuple[bool, float]:
        """Detect if current NDVI is anomalous"""
        current_ndvi = ndvi_data.get("mean", 0.5)
        historical_mean = historical_data.get("ndvi_mean", 0.5)
        historical_std = historical_data.get("ndvi_std", 0.1)

        if historical_std == 0:
            return False, 0.0

        z_score = (current_ndvi - historical_mean) / historical_std

        # Anomaly if more than 2 standard deviations
        is_anomaly = abs(z_score) > 2.0

        return is_anomaly, z_score

    def _investigate_anomaly(
        self,
        ndvi_data: dict,
        weather_data: dict,
        historical_data: dict,
        plot_info: dict
    ) -> dict[str, Any]:
        """Investigate potential causes of anomaly"""

        investigation = {
            "ndvi_drop": ndvi_data.get("mean", 0) < historical_data.get("ndvi_mean", 0),
            "ndvi_change_magnitude": abs(
                ndvi_data.get("mean", 0) - historical_data.get("ndvi_mean", 0)
            ),
            "weather_factors": [],
            "seasonal_factors": [],
            "neighboring_farms": "unknown"  # Would check in production
        }

        # Check weather factors
        if weather_data.get("drought", {}).get("risk_level") in ["medium", "high"]:
            investigation["weather_factors"].append("drought_stress")

        if weather_data.get("heat_stress", {}).get("risk_level") in ["medium", "high"]:
            investigation["weather_factors"].append("heat_stress")

        if weather_data.get("frost", {}).get("risk_level") in ["medium", "high"]:
            investigation["weather_factors"].append("frost_damage")

        # Check seasonal factors
        current_month = datetime.utcnow().month
        if current_month in [11, 12, 1, 2]:  # Winter
            investigation["seasonal_factors"].append("winter_dormancy")

        return investigation

    def _assess_threat(self, investigation: dict) -> dict[str, Any]:
        """Assess threat level based on investigation"""

        threat_level = "low"
        confidence = 0.5

        # High threat if significant NDVI drop with no weather explanation
        if investigation["ndvi_drop"]:
            if investigation["ndvi_change_magnitude"] > 0.2:
                if not investigation["weather_factors"]:
                    threat_level = "high"
                    confidence = 0.85
                else:
                    threat_level = "medium"
                    confidence = 0.70

        # Lower threat if weather explains the change
        if investigation["weather_factors"]:
            if "drought_stress" in investigation["weather_factors"]:
                confidence = 0.80
            if "heat_stress" in investigation["weather_factors"]:
                confidence = 0.75

        # Lower threat if seasonal
        if investigation["seasonal_factors"]:
            threat_level = "low"
            confidence = 0.60

        return {
            "threat_level": threat_level,
            "confidence": confidence,
            "primary_factors": investigation["weather_factors"] or ["unknown_cause"]
        }

    def _make_decision(
        self,
        threat_assessment: dict,
        investigation: dict
    ) -> dict[str, Any]:
        """Make final decision on action"""

        threat_level = threat_assessment["threat_level"]
        confidence = threat_assessment["confidence"]

        if threat_level == "high" and confidence > 0.7:
            action = "escalate_to_diagnostic"
            priority = "high"
        elif threat_level == "medium" and confidence > 0.6:
            action = "escalate_to_diagnostic"
            priority = "medium"
        elif threat_level == "low":
            action = "continue_monitoring"
            priority = "low"
        else:
            action = "request_human_review"
            priority = "medium"

        return {
            "anomaly_detected": True,
            "threat_level": threat_level,
            "confidence": confidence,
            "action": action,
            "priority": priority,
            "investigation_summary": investigation,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _build_reasoning(
        self,
        investigation: dict,
        threat_assessment: dict
    ) -> str:
        """Build human-readable reasoning"""

        reasoning_parts = [
            f"Detected NDVI anomaly with magnitude {investigation['ndvi_change_magnitude']:.3f}."
        ]

        if investigation["weather_factors"]:
            factors = ", ".join(investigation["weather_factors"])
            reasoning_parts.append(f"Weather factors identified: {factors}.")
        else:
            reasoning_parts.append("No obvious weather factors found.")

        if investigation["seasonal_factors"]:
            factors = ", ".join(investigation["seasonal_factors"])
            reasoning_parts.append(f"Seasonal factors: {factors}.")

        reasoning_parts.append(
            f"Assessed threat level as {threat_assessment['threat_level']} "
            f"with {threat_assessment['confidence']:.0%} confidence."
        )

        return " ".join(reasoning_parts)
