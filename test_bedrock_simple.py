#!/usr/bin/env python3
"""Simple Bedrock test to diagnose issues"""

import boto3
import json

# Initialize client
client = boto3.client('bedrock-runtime', region_name='ap-south-1')

# Test model
model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"

# Simple prompt
prompt = "\n\nHuman: Say hello in one word\n\nAssistant:"

body = json.dumps({
    "prompt": prompt,
    "max_tokens_to_sample": 100,
    "temperature": 0.7
})

print(f"Testing model: {model_id}")
print(f"Prompt: {prompt}")
print()

try:
    response = client.invoke_model(
        modelId=model_id,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    completion = response_body.get('completion', '')
    
    print("✓ SUCCESS!")
    print(f"Response: {completion}")
    
except Exception as e:
    print(f"✗ FAILED: {e}")
    print()
    print("This usually means you need to enable model access.")
    print()
    print("To fix:")
    print("1. Go to: https://console.aws.amazon.com/bedrock")
    print("2. Click 'Model access' in the left menu")
    print("3. Click 'Manage model access'")
    print("4. Check the box for 'Claude 3.5 Sonnet v2'")
    print("5. Click 'Request model access'")
    print("6. Wait 2-5 minutes for approval")
    print("7. Run this test again")
