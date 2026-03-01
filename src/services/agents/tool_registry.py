"""
Tool registry for agent actions
"""
import logging
from typing import Dict, Any, Callable, List
from datetime import datetime
from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.models.farmer import Farmer, FarmPlot

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry of tools available to agents"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools"""
        self.tools = {
            "get_farm_data": self.get_farm_data,
            "get_weather_forecast": self.get_weather_forecast,
            "query_knowledge_base": self.query_knowledge_base,
            "check_input_availability": self.check_input_availability,
            "estimate_cost": self.estimate_cost,
            "get_market_prices": self.get_market_prices,
            "schedule_callback": self.schedule_callback,
        }
        logger.info(f"Registered {len(self.tools)} tools")
    
    def get_tool(self, tool_name: str) -> Callable:
        """Get tool by name"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        return self.tools[tool_name]
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools"""
        return [
            {
                "name": name,
                "description": func.__doc__ or "No description"
            }
            for name, func in self.tools.items()
        ]
    
    # Tool implementations
    
    def get_farm_data(self, farmer_id: str, plot_id: str = None) -> Dict[str, Any]:
        """
        Get farm and plot data for a farmer
        
        Args:
            farmer_id: Farmer ID
            plot_id: Optional plot ID
        
        Returns:
            Farm data dictionary
        """
        db: Session = SessionLocal()
        try:
            farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
            
            if not farmer:
                return {"error": "Farmer not found"}
            
            result = {
                "farmer_id": str(farmer.farmer_id),
                "phone": farmer.phone_number,
                "language": farmer.preferred_language,
                "plots": []
            }
            
            plots = farmer.farm_plots
            if plot_id:
                plots = [p for p in plots if str(p.plot_id) == plot_id]
            
            for plot in plots:
                result["plots"].append({
                    "plot_id": str(plot.plot_id),
                    "area_hectares": float(plot.area_hectares),
                    "crop_types": plot.crop_types,
                    "planting_date": plot.planting_date.isoformat() if plot.planting_date else None,
                    "expected_harvest": plot.expected_harvest_date.isoformat() if plot.expected_harvest_date else None,
                })
            
            logger.info(f"Retrieved farm data for farmer {farmer_id}")
            return result
            
        finally:
            db.close()
    
    def get_weather_forecast(self, location: Dict[str, float], days: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast for location
        
        Args:
            location: Dict with lat/lon
            days: Number of days
        
        Returns:
            Weather forecast data
        """
        # This would call the weather client
        # For now, return mock data
        return {
            "location": location,
            "forecast": [
                {
                    "date": (datetime.utcnow().date() + timedelta(days=i)).isoformat(),
                    "temp_max": 32 + i,
                    "temp_min": 22 + i,
                    "humidity": 65,
                    "rainfall_prob": 0.2,
                    "conditions": "Partly cloudy"
                }
                for i in range(days)
            ]
        }
    
    def query_knowledge_base(self, query: str, category: str = "general") -> List[Dict]:
        """
        Query agricultural knowledge base
        
        Args:
            query: Search query
            category: Knowledge category
        
        Returns:
            List of relevant knowledge items
        """
        # This would call the knowledge base
        # For now, return mock data
        return [
            {
                "content": f"Knowledge about: {query}",
                "relevance": 0.85,
                "source": "Agricultural handbook"
            }
        ]
    
    def check_input_availability(
        self,
        input_type: str,
        location: Dict[str, float],
        quantity: float = None
    ) -> Dict[str, Any]:
        """
        Check availability of agricultural inputs
        
        Args:
            input_type: Type of input (fertilizer, pesticide, seeds, etc.)
            location: Location dict
            quantity: Required quantity
        
        Returns:
            Availability information
        """
        # Mock implementation
        return {
            "input_type": input_type,
            "available": True,
            "suppliers": [
                {
                    "name": "Local Agri Store",
                    "distance_km": 5.2,
                    "in_stock": True,
                    "estimated_price": 500
                }
            ],
            "delivery_time_days": 2
        }
    
    def estimate_cost(
        self,
        action_items: List[Dict],
        area_hectares: float
    ) -> Dict[str, Any]:
        """
        Estimate cost of recommended actions
        
        Args:
            action_items: List of action items
            area_hectares: Farm area
        
        Returns:
            Cost estimate
        """
        # Mock implementation
        total_cost = 0
        item_costs = []
        
        for item in action_items:
            # Simple cost estimation
            base_cost = 100  # Base cost per action
            cost = base_cost * area_hectares
            
            item_costs.append({
                "action": item.get("action", "Unknown"),
                "cost": cost,
                "unit": "INR"
            })
            total_cost += cost
        
        return {
            "total_cost": total_cost,
            "currency": "INR",
            "items": item_costs,
            "area_hectares": area_hectares
        }
    
    def get_market_prices(
        self,
        crop_type: str,
        location: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Get current market prices for crop
        
        Args:
            crop_type: Type of crop
            location: Location dict
        
        Returns:
            Market price information
        """
        # Mock implementation
        return {
            "crop_type": crop_type,
            "location": location,
            "current_price": 2500,
            "unit": "INR per quintal",
            "trend": "stable",
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def schedule_callback(
        self,
        farmer_id: str,
        reason: str,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        Schedule callback to farmer
        
        Args:
            farmer_id: Farmer ID
            reason: Reason for callback
            priority: Priority level
        
        Returns:
            Scheduling confirmation
        """
        # Mock implementation
        return {
            "scheduled": True,
            "farmer_id": farmer_id,
            "reason": reason,
            "priority": priority,
            "estimated_time": "Within 2 hours",
            "callback_id": f"cb_{datetime.utcnow().timestamp()}"
        }


# Add missing import
from datetime import timedelta
