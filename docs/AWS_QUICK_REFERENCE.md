# AWS Integration Quick Reference

One-page reference for AWS services integration.

## Environment Variables

```bash
# Provider Selection
LLM_PROVIDER=bedrock              # openai | bedrock
USE_AWS_SERVICES=True             # True | False

# AWS Configuration
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_AUDIO=your-bucket
```

## Quick Commands

### Test Integration
```bash
# Test all providers
python scripts/test_aws_integration.py

# Test specific provider
python -c "from src.services.llm_factory import get_llm; print(get_llm())"
```

### Switch Providers
```bash
# Use AWS
export USE_AWS_SERVICES=True
export LLM_PROVIDER=bedrock

# Use OpenAI
export USE_AWS_SERVICES=False
export LLM_PROVIDER=openai
```

### Enable Bedrock Models
```bash
# List available models
aws bedrock list-foundation-models --region ap-south-1

# Check model access
aws bedrock get-foundation-model \
  --model-identifier anthropic.claude-v2 \
  --region ap-south-1
```

## Code Snippets

### LLM
```python
from src.services.llm_factory import get_llm

llm = get_llm()
response = await llm.generate_completion(messages)
```

### STT
```python
from src.services.speech_factory import get_stt

stt = get_stt()
result = await stt.transcribe(audio_data, language="hi")
```

### TTS
```python
from src.services.speech_factory import get_tts

tts = get_tts()
audio = await tts.synthesize(text, language="hi")
```

## Provider Matrix

| Config | LLM | STT | TTS |
|--------|-----|-----|-----|
| `USE_AWS_SERVICES=False` | OpenAI | Whisper | ElevenLabs |
| `USE_AWS_SERVICES=True` | Bedrock | Transcribe | Polly |
| `LLM_PROVIDER=bedrock` + `USE_AWS_SERVICES=False` | Bedrock | Whisper | ElevenLabs |

## Cost Estimates (10k farmers/month)

| Configuration | Monthly Cost |
|---------------|--------------|
| All OpenAI/ElevenLabs | $600 |
| All AWS | $370 |
| Hybrid (Bedrock + Whisper + ElevenLabs) | $550 |

## IAM Policy (Minimal)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "polly:SynthesizeSpeech",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "*"
    }
  ]
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Model not available" | Enable in Bedrock console |
| "Access denied" | Check IAM permissions |
| "S3 bucket not found" | Create bucket or update env var |
| "Transcribe job failed" | Check S3 permissions |

## Support

- Full Guide: [AWS_INTEGRATION_SUMMARY.md](../AWS_INTEGRATION_SUMMARY.md)
- Deployment: [AWS_DEPLOYMENT.md](../AWS_DEPLOYMENT.md)
- Provider Selection: [PROVIDER_SELECTION_GUIDE.md](PROVIDER_SELECTION_GUIDE.md)
- Checklist: [AWS_INTEGRATION_CHECKLIST.md](../AWS_INTEGRATION_CHECKLIST.md)
