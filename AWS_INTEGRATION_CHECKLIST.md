# AWS Integration Checklist

Use this checklist to verify AWS integration is complete and working.

## Pre-Deployment Checklist

### AWS Account Setup
- [ ] AWS account created
- [ ] IAM user with programmatic access created
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] Verified access: `aws sts get-caller-identity`

### Bedrock Setup
- [ ] Bedrock available in your region (check: ap-south-1, us-east-1, us-west-2)
- [ ] Requested model access in AWS Console
  - [ ] anthropic.claude-v2
  - [ ] amazon.titan-text-express-v1
  - [ ] amazon.titan-embed-text-v1
- [ ] Verified model access: `aws bedrock list-foundation-models --region ap-south-1`

### S3 Setup
- [ ] Created S3 bucket for audio files
- [ ] Enabled versioning on bucket
- [ ] Configured lifecycle policies (optional)
- [ ] Set up bucket permissions for ECS task role

### IAM Permissions
- [ ] Created ECS task execution role
- [ ] Added Bedrock permissions
- [ ] Added Transcribe permissions
- [ ] Added Polly permissions
- [ ] Added S3 permissions
- [ ] Verified permissions with test calls

## Code Integration Checklist

### Environment Configuration
- [ ] Updated `.env` with AWS credentials
  ```bash
  AWS_REGION=ap-south-1
  AWS_ACCESS_KEY_ID=your-key
  AWS_SECRET_ACCESS_KEY=your-secret
  S3_BUCKET_AUDIO=your-bucket
  ```
- [ ] Set provider selection
  ```bash
  LLM_PROVIDER=bedrock
  USE_AWS_SERVICES=True
  ```

### Dependencies
- [ ] Verified boto3 in requirements.txt
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] No import errors when running application

### Provider Factory Tests
- [ ] LLM factory returns correct provider
  ```python
  from src.services.llm_factory import get_llm
  llm = get_llm()
  print(type(llm))  # Should show BedrockProvider
  ```
- [ ] STT factory returns correct provider
  ```python
  from src.services.speech_factory import get_stt
  stt = get_stt()
  print(type(stt))  # Should show TranscribeSTTProvider
  ```
- [ ] TTS factory returns correct provider
  ```python
  from src.services.speech_factory import get_tts
  tts = get_tts()
  print(type(tts))  # Should show PollyTTSProvider
  ```

## Functional Testing Checklist

### Bedrock LLM Testing
- [ ] Test text generation
  ```python
  from src.services.llm_factory import get_llm
  import asyncio
  
  async def test():
      llm = get_llm()
      response = await llm.generate_completion([
          {"role": "user", "content": "What is crop rotation?"}
      ])
      print(response)
  
  asyncio.run(test())
  ```
- [ ] Test embeddings generation
  ```python
  embedding = await llm.generate_embedding("crop health")
  print(len(embedding))  # Should be 1536 for Titan
  ```
- [ ] Verify response quality
- [ ] Check latency (<3 seconds)

### Transcribe STT Testing
- [ ] Test audio transcription
  ```python
  from src.services.speech_factory import get_stt
  import asyncio
  
  async def test():
      stt = get_stt()
      with open("test_audio.mp3", "rb") as f:
          audio_data = f.read()
      result = await stt.transcribe(audio_data, language="hi")
      print(result["text"])
      print(result["confidence"])
  
  asyncio.run(test())
  ```
- [ ] Test language detection
- [ ] Test with different Indian languages
- [ ] Verify S3 upload/cleanup works
- [ ] Check accuracy (>90%)

### Polly TTS Testing
- [ ] Test speech synthesis
  ```python
  from src.services.speech_factory import get_tts
  import asyncio
  
  async def test():
      tts = get_tts()
      audio = await tts.synthesize(
          text="नमस्ते, यह कृषि मित्र है",
          language="hi"
      )
      with open("output.mp3", "wb") as f:
          f.write(audio)
  
  asyncio.run(test())
  ```
- [ ] Test SSML support
- [ ] Test streaming synthesis
- [ ] Verify voice quality
- [ ] Test caching

### Knowledge Base Testing
- [ ] Test with Bedrock embeddings
  ```python
  from src.services.agents.knowledge_base import KnowledgeBase
  import asyncio
  
  async def test():
      kb = KnowledgeBase()
      await kb.seed_initial_knowledge()
      results = await kb.search("crop rotation", n_results=3)
      print(results)
  
  asyncio.run(test())
  ```
- [ ] Verify search accuracy
- [ ] Check embedding dimensions match

### Voice Chatbot Testing
- [ ] Test conversation flow
- [ ] Verify LLM integration
- [ ] Test knowledge base integration
- [ ] Check response quality

## Performance Testing Checklist

### Latency Benchmarks
- [ ] LLM response time: _____ seconds (target: <3s)
- [ ] STT transcription time: _____ seconds (target: <5s)
- [ ] TTS synthesis time: _____ seconds (target: <2s)
- [ ] End-to-end voice interaction: _____ seconds (target: <10s)

### Accuracy Benchmarks
- [ ] LLM response quality: _____ /10
- [ ] STT accuracy: _____ % (target: >90%)
- [ ] TTS naturalness: _____ /10

### Cost Tracking
- [ ] Set up CloudWatch billing alarms
- [ ] Track Bedrock usage
- [ ] Track Transcribe usage
- [ ] Track Polly usage
- [ ] Track S3 storage costs
- [ ] Verify costs are within budget

## Deployment Checklist

### Terraform Infrastructure
- [ ] Updated Terraform with IAM permissions
- [ ] Added Bedrock policy to ECS task role
- [ ] Added Transcribe policy to ECS task role
- [ ] Added Polly policy to ECS task role
- [ ] Added S3 policy to ECS task role
- [ ] Terraform plan reviewed
- [ ] Terraform apply successful

### ECS Configuration
- [ ] Environment variables set in ECS task definition
  ```json
  {
    "name": "USE_AWS_SERVICES",
    "value": "True"
  },
  {
    "name": "LLM_PROVIDER",
    "value": "bedrock"
  }
  ```
- [ ] Secrets configured in Secrets Manager
- [ ] Task role has correct permissions
- [ ] Service deployed successfully

### Application Deployment
- [ ] Docker image built
- [ ] Image pushed to ECR
- [ ] ECS service updated
- [ ] Health check passing
- [ ] Logs showing correct provider selection

## Monitoring Checklist

### CloudWatch Setup
- [ ] Log groups created
- [ ] Metrics configured
- [ ] Alarms set up
  - [ ] High error rate alarm
  - [ ] High latency alarm
  - [ ] Cost threshold alarm
- [ ] Dashboard created

### Application Logs
- [ ] Verify provider selection logged
  ```
  INFO: Using AWS Bedrock as LLM provider
  INFO: Using AWS Transcribe for STT
  INFO: Using AWS Polly for TTS
  ```
- [ ] No error messages in logs
- [ ] Performance metrics logged

## Rollback Plan Checklist

### Fallback to OpenAI
- [ ] Documented rollback procedure
- [ ] Tested switching back to OpenAI
  ```bash
  export USE_AWS_SERVICES=False
  export LLM_PROVIDER=openai
  ```
- [ ] Verified application works with OpenAI
- [ ] Updated ECS task definition with OpenAI config

### Emergency Contacts
- [ ] AWS support contact info documented
- [ ] Team escalation path defined
- [ ] On-call schedule created

## Documentation Checklist

### Updated Documentation
- [ ] README.md updated with AWS info
- [ ] AWS_DEPLOYMENT.md complete
- [ ] AWS_INTEGRATION_SUMMARY.md reviewed
- [ ] PROVIDER_SELECTION_GUIDE.md reviewed
- [ ] .env.example updated
- [ ] Team trained on new configuration

### Runbooks Created
- [ ] Provider switching procedure
- [ ] Troubleshooting guide
- [ ] Cost optimization guide
- [ ] Performance tuning guide

## Post-Deployment Checklist

### Week 1
- [ ] Monitor error rates daily
- [ ] Check latency metrics
- [ ] Review cost reports
- [ ] Gather user feedback
- [ ] Document any issues

### Week 2-4
- [ ] Compare accuracy with OpenAI baseline
- [ ] Optimize based on usage patterns
- [ ] Fine-tune cost controls
- [ ] Update documentation with learnings

### Month 2+
- [ ] Quarterly cost review
- [ ] Performance optimization
- [ ] Consider hybrid approach if needed
- [ ] Plan for scaling

## Success Criteria

### Must Have
- [ ] All AWS services working correctly
- [ ] No increase in error rates
- [ ] Latency within acceptable range (<3s for LLM)
- [ ] Cost reduction achieved (target: 38%)

### Nice to Have
- [ ] Improved latency over OpenAI
- [ ] Better cost optimization than expected
- [ ] Positive user feedback on quality

## Sign-Off

- [ ] Development team tested and approved
- [ ] DevOps team reviewed infrastructure
- [ ] Product team approved quality
- [ ] Finance team approved costs
- [ ] Ready for production deployment

---

**Deployment Date:** _______________

**Deployed By:** _______________

**Approved By:** _______________

**Notes:**
_______________________________________________
_______________________________________________
_______________________________________________
