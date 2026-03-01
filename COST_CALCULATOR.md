# Cost Calculator - Single Farmer vs Scale

## Single Farmer Testing (Your Case)

### Monthly Costs

| Service | Usage | Cost | Free Tier? |
|---------|-------|------|------------|
| **AWS Bedrock** | ~50 requests | $0.50 | ✅ Mostly free |
| **AWS Transcribe** | ~10 minutes | $0.30 | ✅ Free tier |
| **AWS Polly** | ~5,000 chars | $0.20 | ✅ Free tier |
| **AWS S3** | ~100 MB | $0.02 | ✅ Free tier |
| **AWS RDS** | Not needed | $0.00 | Use SQLite |
| **Twilio** | ~5 calls, 5 min each | $0.00 | ✅ $15 trial credit |
| **Weather API** | ~100 calls | $0.00 | ✅ Free tier (1k/day) |
| **Sentinel Hub** | ~4 images | $0.00 | ✅ 30-day trial |
| **TOTAL** | | **~$1-2** | **Mostly FREE!** |

### What's Free?

✅ **Twilio**: $15 trial credit (enough for ~30 hours of calls!)  
✅ **Weather API**: 1,000 calls/day free (you need ~3/day)  
✅ **Sentinel Hub**: 30-day trial with 10,000 processing units  
✅ **AWS Free Tier**: Covers most of your usage  

### What You Pay For?

💰 **AWS Bedrock**: ~$0.50/month (minimal usage)  
💰 **AWS Transcribe**: ~$0.30/month (if exceeds free tier)  
💰 **AWS Polly**: ~$0.20/month (if exceeds free tier)  

**Total out-of-pocket**: ~$1-2/month maximum!

---

## Scaling Comparison

### 1 Farmer (Testing)
- **Cost**: $1-2/month
- **Per farmer**: $1-2/month
- **Free tiers**: Cover most usage
- **Perfect for**: Testing, demo, proof of concept

### 10 Farmers
- **Cost**: $15-20/month
- **Per farmer**: $1.50-2.00/month
- **Free tiers**: Still helpful
- **Good for**: Pilot program, small village

### 100 Farmers
- **Cost**: $120-150/month
- **Per farmer**: $1.20-1.50/month
- **Free tiers**: Exhausted
- **Good for**: Multiple villages, beta testing

### 1,000 Farmers
- **Cost**: $800-1,000/month
- **Per farmer**: $0.80-1.00/month
- **Free tiers**: Not applicable
- **Good for**: District-level deployment

### 10,000 Farmers (Full Scale)
- **Cost**: $1,130/month
- **Per farmer**: $0.113/month
- **Free tiers**: Not applicable
- **Good for**: State-level deployment

---

## Cost Breakdown by Service (10,000 Farmers)

### AWS Services ($570/month)

| Service | Usage | Cost | Per Farmer |
|---------|-------|------|------------|
| Bedrock (Claude) | 100k requests | $150 | $0.015 |
| Transcribe | 50k minutes | $120 | $0.012 |
| Polly | 50k chars | $100 | $0.010 |
| S3 | 100 GB | $25 | $0.0025 |
| RDS (PostgreSQL) | db.t3.medium | $75 | $0.0075 |
| ECS Fargate | 2 vCPU, 4GB | $50 | $0.005 |
| CloudWatch | Logs + Metrics | $30 | $0.003 |
| Lambda | 1M invocations | $20 | $0.002 |

### External Services ($560/month)

| Service | Usage | Cost | Per Farmer |
|---------|-------|------|------------|
| Twilio | 50k min calls | $425 | $0.0425 |
| Weather API | 300k calls | $60 | $0.006 |
| Sentinel Hub | 40k images | $75 | $0.0075 |

---

## Cost Optimization Tips

### For Single Farmer Testing

1. **Use free tiers**: All services have generous free tiers
2. **Use SQLite**: No need for RDS database
3. **Skip Redis**: Not needed for single farmer
4. **Use Twilio trial**: $15 credit lasts months
5. **Minimize calls**: Test with 1-2 calls/week

**Savings**: ~95% (from $20 to $1-2)

### For 100 Farmers

1. **Use AWS free tier**: First year benefits
2. **Batch processing**: Process multiple farmers together
3. **Cache weather data**: Reduce API calls
4. **Optimize images**: Request only needed satellite bands
5. **Use spot instances**: 70% cheaper for non-critical workloads

**Savings**: ~30% (from $150 to $105)

### For 10,000 Farmers

1. **Reserved instances**: 40% cheaper than on-demand
2. **Savings plans**: Commit to 1-3 years for discounts
3. **S3 Intelligent Tiering**: Auto-optimize storage costs
4. **CloudFront CDN**: Cache static content
5. **Batch API calls**: Reduce per-call costs
6. **Negotiate rates**: Volume discounts with Twilio, Weather API

**Savings**: ~25% (from $1,130 to $850)

---

## ROI Analysis

### Cost per Farmer per Year

| Scale | Monthly | Yearly | Benefit to Farmer |
|-------|---------|--------|-------------------|
| 1 farmer | $1-2 | $12-24 | Early warnings, better yields |
| 10 farmers | $1.50 | $18 | Prevent crop loss (~$500/year) |
| 100 farmers | $1.20 | $14.40 | Increase yield by 10-15% |
| 1,000 farmers | $0.80 | $9.60 | Save water, reduce pesticides |
| 10,000 farmers | $0.11 | $1.32 | Massive impact at scale |

### Value Proposition

**For 1 farmer**:
- Cost: $1-2/month
- Benefit: Prevent one crop failure = $500 saved
- ROI: 25,000% (if prevents one failure per year)

**For 10,000 farmers**:
- Cost: $1,130/month = $13,560/year
- Benefit: 10% yield increase = $5M saved (assuming $50/farmer/year)
- ROI: 36,800%

---

## Free Tier Limits

### AWS Free Tier (First 12 Months)

| Service | Free Tier | Your Usage (1 farmer) | Covered? |
|---------|-----------|----------------------|----------|
| Bedrock | 1M tokens | ~50k tokens | ✅ Yes |
| Transcribe | 60 minutes | ~10 minutes | ✅ Yes |
| Polly | 5M chars | ~5k chars | ✅ Yes |
| S3 | 5 GB | ~100 MB | ✅ Yes |
| Lambda | 1M requests | ~1k requests | ✅ Yes |

### Twilio Trial

- **Credit**: $15
- **Calls**: ~30 hours of calls
- **Your usage**: ~25 minutes/month
- **Lasts**: ~72 months! (6 years)

### Weather API Free Tier

- **Limit**: 1,000 calls/day
- **Your usage**: ~3 calls/day
- **Covered**: ✅ Completely

### Sentinel Hub Trial

- **Duration**: 30 days
- **Processing units**: 10,000
- **Your usage**: ~40 units/month
- **Covered**: ✅ Completely

---

## When to Upgrade

### From Free Tier to Paid

**Trigger**: When you exceed free tier limits

**For 1 farmer**: Never (stays within free tier)  
**For 10 farmers**: Month 2-3 (AWS free tier exhausted)  
**For 100 farmers**: Immediately (exceeds all limits)  

### From Trial to Paid

**Twilio**: When $15 credit exhausted (~30 hours of calls)  
**Sentinel Hub**: After 30 days or 10,000 processing units  
**Weather API**: When exceeding 1,000 calls/day  

---

## Cost Monitoring

### Set Up Billing Alerts

```powershell
# AWS Billing Alert
aws cloudwatch put-metric-alarm \
  --alarm-name "KrishiMitra-Billing-Alert" \
  --alarm-description "Alert when costs exceed $10" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

### Check Current Costs

```powershell
# Check AWS costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost

# Check Twilio balance
# Visit: https://console.twilio.com/billing

# Check Weather API usage
# Visit: https://home.openweathermap.org/statistics

# Check Sentinel Hub usage
# Visit: https://apps.sentinel-hub.com/dashboard
```

---

## Summary

### Single Farmer Testing (Your Case)

✅ **Total cost**: $1-2/month  
✅ **Mostly FREE** (using free tiers and trials)  
✅ **Perfect for**: Testing, demo, proof of concept  
✅ **No commitment**: Cancel anytime  
✅ **Full functionality**: All features work  

### Recommendation

**Start with 1 farmer** (you!) to:
1. Test all features
2. Validate the concept
3. Get comfortable with the system
4. Show to potential users/investors
5. Scale when ready

**Cost**: Almost nothing! 🎉
