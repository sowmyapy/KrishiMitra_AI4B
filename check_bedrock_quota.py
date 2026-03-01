"""
Check AWS Bedrock quotas and limits
"""
import boto3
import json
from datetime import datetime

def check_bedrock_quotas():
    """Check Bedrock service quotas"""
    
    # Initialize clients
    bedrock = boto3.client('bedrock', region_name='ap-south-1')
    service_quotas = boto3.client('service-quotas', region_name='ap-south-1')
    
    print("=" * 60)
    print("AWS Bedrock Quota Check")
    print("=" * 60)
    print(f"Region: ap-south-1")
    print(f"Time: {datetime.now()}")
    print()
    
    # Check available models
    print("Available Models:")
    print("-" * 60)
    try:
        response = bedrock.list_foundation_models()
        for model in response.get('modelSummaries', []):
            model_id = model.get('modelId', 'N/A')
            model_name = model.get('modelName', 'N/A')
            provider = model.get('providerName', 'N/A')
            
            # Only show models we might use
            if any(x in model_id.lower() for x in ['llama', 'claude', 'titan', 'nova']):
                print(f"  {provider}: {model_name}")
                print(f"    ID: {model_id}")
                print()
    except Exception as e:
        print(f"  Error listing models: {e}")
    
    # Check service quotas
    print("\nService Quotas:")
    print("-" * 60)
    try:
        # Get Bedrock quotas
        response = service_quotas.list_service_quotas(
            ServiceCode='bedrock'
        )
        
        for quota in response.get('Quotas', []):
            quota_name = quota.get('QuotaName', 'N/A')
            value = quota.get('Value', 'N/A')
            unit = quota.get('Unit', '')
            
            print(f"  {quota_name}: {value} {unit}")
    except Exception as e:
        print(f"  Error getting quotas: {e}")
        print(f"  This might be a permissions issue or quotas not available in this region")
    
    # Check CloudWatch metrics for usage
    print("\nRecent Usage (CloudWatch):")
    print("-" * 60)
    try:
        cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
        
        # Get metrics for the last hour
        from datetime import timedelta
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)
        
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Bedrock',
            MetricName='Invocations',
            Dimensions=[
                {
                    'Name': 'ModelId',
                    'Value': 'meta.llama3-8b-instruct-v1:0'
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Sum']
        )
        
        datapoints = response.get('Datapoints', [])
        if datapoints:
            total_invocations = sum(dp.get('Sum', 0) for dp in datapoints)
            print(f"  Total invocations (last hour): {total_invocations}")
        else:
            print(f"  No usage data available (might be too recent)")
    except Exception as e:
        print(f"  Error getting usage: {e}")
    
    print("\n" + "=" * 60)
    print("Recommendations:")
    print("=" * 60)
    print("1. If you see 'ThrottlingException', you've hit rate limits")
    print("2. Free tier limits are typically very low (10-20 requests/minute)")
    print("3. Consider requesting a quota increase in AWS Service Quotas console")
    print("4. Or wait 24 hours for quota to reset")
    print("5. For production, you'll need to request higher quotas")
    print()

if __name__ == "__main__":
    check_bedrock_quotas()
