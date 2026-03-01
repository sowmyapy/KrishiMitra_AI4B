# Provider Selection Guide

Quick reference for choosing between OpenAI/ElevenLabs and AWS services.

## Quick Start

### Use OpenAI + ElevenLabs (Default)

```bash
# .env
LLM_PROVIDER=openai
USE_AWS_SERVICES=False

# Required API keys
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
```

### Use AWS Services

```bash
# .env
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# Required AWS config
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET_AUDIO=your-bucket
```

## Provider Matrix

| Service | OpenAI/ElevenLabs | AWS Native | Hybrid Option |
|---------|-------------------|------------|---------------|
| **LLM** | OpenAI GPT-4 | AWS Bedrock Claude v2 | ✓ Configurable |
| **STT** | OpenAI Whisper | AWS Transcribe | ✓ Configurable |
| **TTS** | ElevenLabs | AWS Polly | ✓ Configurable |
| **Embeddings** | OpenAI | Bedrock Titan | ✓ Configurable |

## Configuration Options

### Option 1: All OpenAI/ElevenLabs
```bash
LLM_PROVIDER=openai
USE_AWS_SERVICES=False
```
- ✅ Best quality for Indian languages
- ✅ Easy setup
- ❌ Higher cost (~$600/month for 10k farmers)

### Option 2: All AWS
```bash
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True
```
- ✅ Lowest cost (~$370/month for 10k farmers)
- ✅ Data stays in AWS
- ❌ Limited Indian language support for TTS

### Option 3: Hybrid (Recommended)
```bash
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=False
```
- ✅ Cost-effective LLM
- ✅ Best quality STT/TTS
- ✅ Balanced approach
- Cost: ~$450/month for 10k farmers

## Code Examples

### Using LLM (Provider-Agnostic)

```python
from src.services.llm_factory import get_llm

# Automatically uses configured provider
llm = get_llm()

# Generate text
response = await llm.generate_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What is crop rotation?"}
    ],
    temperature=0.7,
    max_tokens=500
)

# Generate embeddings
embedding = await llm.generate_embedding("crop health monitoring")
```

### Using STT (Provider-Agnostic)

```python
from src.services.speech_factory import get_stt

# Automatically uses configured provider
stt = get_stt()

# Transcribe audio
result = await stt.transcribe(
    audio_data=audio_bytes,
    language="hi",  # Hindi
    format="mp3"
)

print(result["text"])
print(result["confidence"])
```

### Using TTS (Provider-Agnostic)

```python
from src.services.speech_factory import get_tts

# Automatically uses configured provider
tts = get_tts()

# Synthesize speech
audio = await tts.synthesize(
    text="नमस्ते, यह कृषि मित्र है",
    language="hi",
    voice_gender="male"
)

# Save to file
with open("output.mp3", "wb") as f:
    f.write(audio)
```

## Language Support Comparison

### STT (Speech-to-Text)

| Language | Whisper | Transcribe |
|----------|---------|------------|
| Hindi | ✅ Excellent | ✅ Good |
| Bengali | ✅ Excellent | ✅ Good |
| Telugu | ✅ Excellent | ✅ Good |
| Marathi | ✅ Excellent | ✅ Good |
| Tamil | ✅ Excellent | ✅ Good |
| Gujarati | ✅ Excellent | ✅ Good |
| Kannada | ✅ Excellent | ✅ Good |
| Malayalam | ✅ Excellent | ✅ Good |
| Punjabi | ✅ Excellent | ✅ Good |
| Odia | ✅ Excellent | ❌ Not supported |
| English | ✅ Excellent | ✅ Excellent |

### TTS (Text-to-Speech)

| Language | ElevenLabs | Polly |
|----------|------------|-------|
| Hindi | ✅ Excellent | ✅ Good (Aditi) |
| Bengali | ✅ Excellent | ❌ Not supported |
| Telugu | ✅ Excellent | ❌ Not supported |
| Marathi | ✅ Excellent | ❌ Not supported |
| Tamil | ✅ Excellent | ❌ Not supported |
| Gujarati | ✅ Excellent | ❌ Not supported |
| Kannada | ✅ Excellent | ❌ Not supported |
| Malayalam | ✅ Excellent | ❌ Not supported |
| Punjabi | ✅ Excellent | ❌ Not supported |
| Odia | ✅ Excellent | ❌ Not supported |
| English | ✅ Excellent | ✅ Good (Raveena) |

## Performance Comparison

### Latency

| Service | OpenAI/ElevenLabs | AWS |
|---------|-------------------|-----|
| LLM | ~2-3s | ~2-3s |
| STT | ~1-2s | ~3-5s (includes S3 upload) |
| TTS | ~1-2s | ~1-2s |

### Accuracy

| Service | OpenAI/ElevenLabs | AWS |
|---------|-------------------|-----|
| LLM | Excellent | Excellent |
| STT | 95%+ | 90-95% |
| TTS | Natural | Good |

## Cost Breakdown (10,000 farmers/month)

### OpenAI + ElevenLabs
- GPT-4 API: $300
- Whisper API: $100
- ElevenLabs: $200
- **Total: $600/month**

### AWS Services
- Bedrock Claude: $250
- Transcribe: $80
- Polly: $40
- **Total: $370/month**

### Hybrid (Bedrock + Whisper + ElevenLabs)
- Bedrock Claude: $250
- Whisper API: $100
- ElevenLabs: $200
- **Total: $550/month**

## Decision Tree

```
Do you need support for 10+ Indian languages in TTS?
├─ YES → Use ElevenLabs for TTS
│   └─ Do you want to minimize cost?
│       ├─ YES → Use Bedrock for LLM, Whisper for STT
│       └─ NO → Use OpenAI for everything
│
└─ NO (Hindi + English only is fine)
    └─ Use AWS services for everything (lowest cost)
```

## Testing Different Providers

### Test OpenAI
```bash
export LLM_PROVIDER=openai
export USE_AWS_SERVICES=False
python -c "
from src.services.llm_factory import get_llm
import asyncio
async def test():
    llm = get_llm()
    print(await llm.generate_completion([{'role': 'user', 'content': 'Hello'}]))
asyncio.run(test())
"
```

### Test Bedrock
```bash
export LLM_PROVIDER=bedrock
export USE_AWS_SERVICES=True
python -c "
from src.services.llm_factory import get_llm
import asyncio
async def test():
    llm = get_llm()
    print(await llm.generate_completion([{'role': 'user', 'content': 'Hello'}]))
asyncio.run(test())
"
```

## Troubleshooting

### "Bedrock model not available"
```bash
# Enable models in AWS Console
# Go to: Bedrock > Model access > Request model access
# Select: Claude v2, Titan Text, Titan Embeddings
```

### "Transcribe job failed"
```bash
# Check S3 bucket exists and has correct permissions
aws s3 ls s3://$S3_BUCKET_AUDIO

# Check IAM permissions for Transcribe
aws iam get-role-policy --role-name YourECSTaskRole --policy-name TranscribePolicy
```

### "Polly synthesis failed"
```bash
# Check IAM permissions
aws polly describe-voices --language-code hi-IN

# Test synthesis
aws polly synthesize-speech \
  --output-format mp3 \
  --voice-id Aditi \
  --text "नमस्ते" \
  output.mp3
```

## Best Practices

1. **Development:** Use OpenAI/ElevenLabs (easier setup)
2. **Staging:** Test with AWS services
3. **Production:** Use hybrid approach (Bedrock + Whisper + ElevenLabs)
4. **Monitor:** Track costs and performance metrics
5. **Fallback:** Implement retry logic with alternative provider

## Environment Variables Reference

```bash
# Provider Selection
LLM_PROVIDER=openai              # openai | bedrock
USE_AWS_SERVICES=False           # True | False

# OpenAI
OPENAI_API_KEY=sk-...

# ElevenLabs
ELEVENLABS_API_KEY=...

# AWS
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET_AUDIO=krishimitra-audio
```

## Migration Checklist

Migrating from OpenAI to AWS:

- [ ] Enable Bedrock models in AWS Console
- [ ] Create S3 bucket for audio files
- [ ] Configure IAM permissions
- [ ] Update environment variables
- [ ] Test LLM generation
- [ ] Test STT transcription
- [ ] Test TTS synthesis
- [ ] Monitor costs
- [ ] Compare quality metrics
- [ ] Update documentation

---

**Need Help?** Check [AWS_INTEGRATION_SUMMARY.md](../AWS_INTEGRATION_SUMMARY.md) for detailed information.
