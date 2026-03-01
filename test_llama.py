#!/usr/bin/env python3
"""Test Meta Llama 3 model"""

import boto3
import json

client = boto3.client('bedrock-runtime', region_name='ap-south-1')

# Test Meta Llama 3 8B
model_id = "meta.llama3-8b-instruct-v1:0"

body = json.dumps({
    "prompt": "Hello, how are you?",
    "max_gen_len": 50,
    "temperature": 0.5
})

print(f"Testing model: {model_id}")

try:
    response = client.invoke_model(
        modelId=model_id,
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    print("✓ SUCCESS!")
    print(f"Response: {response_body}")
    
except Exception as e:
    print(f"✗ FAILED: {e}")
