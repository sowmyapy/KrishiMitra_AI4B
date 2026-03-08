"""
Advisory Agent - Personalized advisory generation
"""
import logging
from datetime import datetime
from typing import Any

from src.services.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AdvisoryAgent(BaseAgent):
    """Agent for generating personalized agricultural advisories"""

    def __init__(self, tools, knowledge_base):
        super().__init__(
            name="Advisory Agent",
            role="personalized advisory generation and action planning",
            tools=tools,
            knowledge_base=knowledge_base
        )

    def _get_responsibilities(self) -> str:
        return """- Generate personalized, actionable advisories
- Consider farmer's resources and constraints
- Estimate costs and check input availability
- Provide alternative solutions
- Adapt language and cultural context
- Ensure recommendations are practical and safe"""

    def think(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Generate personalized advisory

        Args:
            context: Contains diagnosis, farmer_profile, plot_info, constraints

        Returns:
            Personalized advisory with actions
        """
        diagnosis = context.get("diagnosis", {})
        farmer_profile = context.get("farmer_profile", {})
        plot_info = context.get("plot_info", {})
        constraints = context.get("constraints", {})

        # Step 1: Get relevant knowledge
        knowledge = self._retrieve_knowledge(diagnosis, plot_info)

        # Step 2: Generate primary recommendations
        primary_actions = self._generate_primary_actions(
            diagnosis,
            knowledge,
            plot_info
        )

        # Step 3: Check feasibility and costs
        feasible_actions = self._check_feasibility(
            primary_actions,
            farmer_profile,
            constraints
        )

        # Step 4: Generate alternatives if needed
        if not feasible_actions:
            feasible_actions = self._generate_alternatives(
                diagnosis,
                knowledge,
                constraints
            )

        # Step 5: Build advisory
        advisory = self._build_advisory(
            feasible_actions,
            diagnosis,
            farmer_profile
        )

        # Log decision
        reasoning = self._build_reasoning(diagnosis, feasible_actions, constraints)
        self.log_decision(advisory, context, reasoning)

        return advisory

    def _retrieve_knowledge(
        self,
        diagnosis: dict,
        plot_info: dict
    ) -> list[dict]:
        """Retrieve relevant knowledge from knowledge base"""

        stress_type = diagnosis.get("stress_type", "unknown")
        crop_types = plot_info.get("crop_types", [])

        # Query knowledge base
        query = f"Treatment for {stress_type} in {', '.join(crop_types)}"

        knowledge = self.knowledge_base.search(
            query,
            collection_name="crop_management",
            n_results=3
        )

        return knowledge

    def _generate_primary_actions(
        self,
        diagnosis: dict,
        knowledge: list[dict],
        plot_info: dict
    ) -> list[dict]:
        """Generate primary recommended actions"""

        stress_type = diagnosis.get("stress_type", "unknown")
        diagnosis.get("risk_score", 0)

        actions = []

        # Water stress actions
        if stress_type == "water_stress":
            actions.append({
                "action": "immediate_irrigation",
                "description": "Irrigate the field immediately to restore soil moisture",
                "priority": "high",
                "timeframe": "within 24 hours",
                "inputs_needed": ["water"],
                "estimated_cost_per_hectare": 200
            })
            actions.append({
                "action": "mulching",
                "description": "Apply organic mulch to conserve soil moisture",
                "priority": "medium",
                "timeframe": "within 3 days",
                "inputs_needed": ["organic_mulch"],
                "estimated_cost_per_hectare": 500
            })

        # Heat stress actions
        elif stress_type == "heat_stress":
            actions.append({
                "action": "increase_irrigation_frequency",
                "description": "Increase irrigation frequency to twice daily during hot hours",
                "priority": "high",
                "timeframe": "immediate",
                "inputs_needed": ["water"],
                "estimated_cost_per_hectare": 300
            })
            actions.append({
                "action": "shade_netting",
                "description": "Install shade nets to reduce heat stress (if feasible)",
                "priority": "medium",
                "timeframe": "within 2 days",
                "inputs_needed": ["shade_net"],
                "estimated_cost_per_hectare": 2000
            })

        # Nutrient deficiency actions
        elif stress_type == "nutrient_deficiency":
            actions.append({
                "action": "foliar_spray",
                "description": "Apply foliar spray with micronutrients",
                "priority": "high",
                "timeframe": "within 2 days",
                "inputs_needed": ["micronutrient_spray"],
                "estimated_cost_per_hectare": 400
            })
            actions.append({
                "action": "soil_amendment",
                "description": "Apply balanced NPK fertilizer based on soil test",
                "priority": "medium",
                "timeframe": "within 1 week",
                "inputs_needed": ["npk_fertilizer"],
                "estimated_cost_per_hectare": 800
            })

        # Pest/disease actions
        elif stress_type == "pest_disease":
            actions.append({
                "action": "pest_inspection",
                "description": "Conduct thorough field inspection to identify pest/disease",
                "priority": "high",
                "timeframe": "within 24 hours",
                "inputs_needed": [],
                "estimated_cost_per_hectare": 0
            })
            actions.append({
                "action": "organic_pesticide",
                "description": "Apply neem-based organic pesticide",
                "priority": "high",
                "timeframe": "within 2 days",
                "inputs_needed": ["neem_oil"],
                "estimated_cost_per_hectare": 600
            })

        # Frost damage actions
        elif stress_type == "frost_damage":
            actions.append({
                "action": "frost_protection",
                "description": "Cover crops with protective material during cold nights",
                "priority": "high",
                "timeframe": "before sunset",
                "inputs_needed": ["protective_cover"],
                "estimated_cost_per_hectare": 1000
            })

        return actions

    def _check_feasibility(
        self,
        actions: list[dict],
        farmer_profile: dict,
        constraints: dict
    ) -> list[dict]:
        """Check feasibility of actions based on constraints"""

        max_budget = constraints.get("max_budget", float('inf'))
        area_hectares = constraints.get("area_hectares", 1.0)

        feasible_actions = []

        for action in actions:
            total_cost = action["estimated_cost_per_hectare"] * area_hectares

            # Check budget constraint
            if total_cost <= max_budget:
                action["total_cost"] = total_cost
                action["feasible"] = True
                feasible_actions.append(action)
            else:
                action["total_cost"] = total_cost
                action["feasible"] = False
                action["reason"] = "exceeds_budget"

        return [a for a in feasible_actions if a["feasible"]]

    def _generate_alternatives(
        self,
        diagnosis: dict,
        knowledge: list[dict],
        constraints: dict
    ) -> list[dict]:
        """Generate alternative low-cost actions"""

        stress_type = diagnosis.get("stress_type", "unknown")

        alternatives = []

        # Low-cost alternatives
        if stress_type == "water_stress":
            alternatives.append({
                "action": "reduce_evaporation",
                "description": "Reduce evaporation by irrigating early morning or evening",
                "priority": "medium",
                "timeframe": "immediate",
                "inputs_needed": [],
                "estimated_cost_per_hectare": 0,
                "total_cost": 0,
                "feasible": True
            })

        elif stress_type == "heat_stress":
            alternatives.append({
                "action": "adjust_irrigation_timing",
                "description": "Irrigate during cooler hours to reduce heat stress",
                "priority": "medium",
                "timeframe": "immediate",
                "inputs_needed": [],
                "estimated_cost_per_hectare": 0,
                "total_cost": 0,
                "feasible": True
            })

        return alternatives

    def _build_advisory(
        self,
        actions: list[dict],
        diagnosis: dict,
        farmer_profile: dict
    ) -> dict[str, Any]:
        """Build final advisory message"""

        # Sort actions by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        actions.sort(key=lambda x: priority_order.get(x["priority"], 3))

        # Build summary
        stress_type = diagnosis.get("stress_type", "unknown").replace("_", " ").title()
        risk_score = diagnosis.get("risk_score", 0)

        summary = f"Your crop is showing signs of {stress_type} with risk score {risk_score:.0f}/100."

        # Build action list
        action_items = []
        total_cost = 0

        for i, action in enumerate(actions, 1):
            action_items.append({
                "step": i,
                "action": action["action"],
                "description": action["description"],
                "priority": action["priority"],
                "timeframe": action["timeframe"],
                "cost": action.get("total_cost", 0)
            })
            total_cost += action.get("total_cost", 0)

        advisory = {
            "summary": summary,
            "stress_type": diagnosis.get("stress_type"),
            "risk_score": risk_score,
            "actions": action_items,
            "total_estimated_cost": total_cost,
            "language": farmer_profile.get("language", "en"),
            "generated_at": datetime.utcnow().isoformat()
        }

        return advisory

    def _build_reasoning(
        self,
        diagnosis: dict,
        actions: list[dict],
        constraints: dict
    ) -> str:
        """Build reasoning explanation"""

        reasoning_parts = [
            f"Diagnosed {diagnosis.get('stress_type')} with risk score {diagnosis.get('risk_score', 0):.0f}.",
            f"Generated {len(actions)} feasible actions considering budget constraint of ₹{constraints.get('max_budget', 0)}.",
        ]

        if actions:
            high_priority = [a for a in actions if a["priority"] == "high"]
            reasoning_parts.append(
                f"Prioritized {len(high_priority)} high-priority actions for immediate implementation."
            )

        return " ".join(reasoning_parts)
