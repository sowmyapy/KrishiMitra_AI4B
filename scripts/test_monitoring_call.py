"""
Test script to verify monitoring service calls farmers with high risk
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.database import SessionLocal
from src.models.farmer import Farmer, FarmPlot
from src.services.monitoring.auto_monitor_service import AutoMonitorService


async def test_monitoring_call():
    """Test monitoring service with manual risk calculation"""
    
    print("=" * 60)
    print("Testing Automated Monitoring - Voice Call Functionality")
    print("=" * 60)
    
    # Initialize monitoring service
    monitor_service = AutoMonitorService()
    
    # Get a farmer from database
    db = SessionLocal()
    try:
        farmer = db.query(Farmer).first()
        
        if not farmer:
            print("❌ No farmers found in database")
            return
        
        print(f"\n📞 Testing with Farmer: {farmer.phone_number}")
        print(f"   Language: {farmer.preferred_language}")
        print(f"   Timezone: {farmer.timezone}")
        
        # Get farmer's plot
        plot = db.query(FarmPlot).filter(FarmPlot.farmer_id == farmer.farmer_id).first()
        
        if not plot:
            print("❌ No plot found for farmer")
            return
        
        print(f"   Plot Location: ({plot.latitude}, {plot.longitude})")
        
        # Calculate risk score
        print("\n🔍 Calculating risk score...")
        risk_score = await monitor_service._calculate_risk_score(farmer, plot, db)
        print(f"   Risk Score: {risk_score}/100")
        
        # Check thresholds
        print(f"\n📊 Thresholds:")
        print(f"   Advisory Threshold: {monitor_service.risk_threshold}")
        print(f"   Call Threshold: {monitor_service.call_threshold}")
        
        # Test advisory generation
        if risk_score >= monitor_service.risk_threshold:
            print(f"\n✅ Risk score ({risk_score}) >= Advisory threshold ({monitor_service.risk_threshold})")
            print("   Generating advisory...")
            
            advisory_created = await monitor_service._generate_advisory(farmer, db)
            
            if advisory_created:
                print("   ✅ Advisory created successfully")
                
                # Test call if risk is high enough
                if risk_score >= monitor_service.call_threshold:
                    print(f"\n✅ Risk score ({risk_score}) >= Call threshold ({monitor_service.call_threshold})")
                    
                    # Check calling hours
                    can_call = await monitor_service.voice_service.check_calling_hours(farmer.timezone)
                    
                    if can_call:
                        print("   ✅ Within calling hours (9 AM - 7 PM)")
                        print("   📞 Initiating voice call...")
                        
                        try:
                            await monitor_service._make_call(farmer)
                            print("   ✅ Voice call initiated successfully!")
                            print(f"   📱 Call sent to: {farmer.phone_number}")
                        except Exception as e:
                            print(f"   ❌ Failed to make call: {e}")
                    else:
                        print("   ⏰ Outside calling hours (9 AM - 7 PM)")
                        print("   ℹ️  Call will be skipped")
                else:
                    print(f"\n⚠️  Risk score ({risk_score}) < Call threshold ({monitor_service.call_threshold})")
                    print("   ℹ️  Advisory created but no call will be made")
            else:
                print("   ❌ Failed to create advisory")
        else:
            print(f"\n⚠️  Risk score ({risk_score}) < Advisory threshold ({monitor_service.risk_threshold})")
            print("   ℹ️  No action will be taken")
        
        print("\n" + "=" * 60)
        print("Test Complete")
        print("=" * 60)
        
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(test_monitoring_call())
