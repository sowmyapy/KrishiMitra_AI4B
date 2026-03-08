# KrishiMitra Demo Video Guide

## Video Overview
**Duration**: 3-5 minutes
**Target Audience**: Hackathon judges, potential users, investors
**Goal**: Showcase AI-powered agricultural advisory system with real-time monitoring

---

## Equipment & Software Needed

### Recording Tools
- **Screen Recording**: OBS Studio (free) or Loom
- **Video Editing**: DaVinci Resolve (free) or CapCut
- **Audio**: Clear microphone or phone with good audio
- **Phone Recording**: For showing voice call feature

### Preparation
- Clean browser (close unnecessary tabs)
- Test farmer data: +918095666788 (Hindi farmer)
- Fresh advisory generated
- Stable internet connection

---

## Video Structure

### 1. OPENING (15 seconds)
**Visual**: Title card with logo
**Script**: 
> "KrishiMitra - AI-powered agricultural advisory system that helps farmers make data-driven decisions using satellite imagery, weather data, and AI-generated insights in their local language."

**On Screen Text**:
- KrishiMitra
- AI for Bharat Hackathon 2026
- Built with AWS Bedrock, Sentinel Hub, OpenWeather

---

### 2. PROBLEM STATEMENT (20 seconds)
**Visual**: Show statistics or images
**Script**:
> "Indian farmers face challenges: unpredictable weather, crop diseases, and lack of timely information. Most advisories are in English, creating a language barrier for 80% of farmers."

**On Screen Text**:
- 🌾 140M+ farmers in India
- 🗣️ Language barrier in agricultural advice
- 📱 Need for accessible, timely information

---

### 3. SOLUTION OVERVIEW (20 seconds)
**Visual**: Architecture diagram or feature list
**Script**:
> "KrishiMitra combines satellite imagery, weather forecasting, and AI to deliver personalized advisories in Hindi and Telugu through voice calls."

**On Screen Text**:
- 🛰️ Real-time satellite monitoring
- 🤖 AI-powered advisories (AWS Bedrock)
- 📞 Voice calls in local languages
- ☁️ Deployed on AWS

---

### 4. FEATURE DEMO - Dashboard (30 seconds)

#### Scene 1: Farmers List
**Action**: 
1. Open http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
2. Show farmers list page
3. Highlight farmer cards with language badges

**Script**:
> "The dashboard shows all registered farmers. Each farmer has their preferred language - Hindi or Telugu. Let's look at one farmer's details."

**Highlight**:
- Clean, intuitive UI
- Language preference visible
- Multiple farmers supported

---

### 5. FEATURE DEMO - Farmer Details (45 seconds)

#### Scene 2: Farmer Profile
**Action**:
1. Click on Hindi farmer (+918095666788)
2. Show farmer details page
3. Point out farm plots section

**Script**:
> "Here's Rajesh Kumar, a farmer from Maharashtra. He has 2 hectares of wheat cultivation. The system tracks his farm location and crop type."

#### Scene 3: Farm Plots
**Action**:
1. Scroll to plots section
2. Show plot details with coordinates

**Script**:
> "Each plot is geo-tagged with precise coordinates, allowing us to fetch satellite imagery and weather data for that specific location."

---

### 6. FEATURE DEMO - Advisory Generation (60 seconds)

#### Scene 4: Generate Advisory
**Action**:
1. Click "Generate Advisory" button
2. Show loading state
3. Display generated advisory in Hindi

**Script**:
> "Now, let's generate a personalized advisory. The system analyzes satellite data, weather forecasts, and crop conditions using AWS Bedrock AI."

**Highlight**:
- Advisory in Hindi (show text)
- Includes weather forecast
- Crop-specific recommendations
- Irrigation and fertilizer advice

**On Screen**: Show advisory text with translation:
```
नमस्ते राजेश कुमार जी,

आज का मौसम: तापमान 28°C, आर्द्रता 65%

सिंचाई सलाह: अगले 3 दिनों में हल्की बारिश की संभावना...
```

---

### 7. FEATURE DEMO - Voice Call (45 seconds)

#### Scene 5: Initiate Voice Call
**Action**:
1. Click "Make Voice Call" button
2. Show success message
3. **Switch to phone recording**
4. Show incoming call on phone
5. Answer call and play audio

**Script**:
> "The most powerful feature - farmers receive advisories via voice call in their language. Let me demonstrate..."

**Phone Screen**:
- Show incoming call from +17752270557
- Answer call
- Play advisory audio in Hindi
- Show call duration

**Script (during call)**:
> "The farmer hears the complete advisory in Hindi, making it accessible even for those who can't read."

---

### 8. FEATURE DEMO - Monitoring (30 seconds)

#### Scene 6: Monitoring Dashboard
**Action**:
1. Navigate to Monitoring page
2. Show monitoring controls
3. Click "Check Now" button
4. Show monitoring results

**Script**:
> "The monitoring system continuously tracks crop health using satellite imagery and weather data. Farmers receive alerts for any anomalies."

**Highlight**:
- Real-time monitoring
- Automated checks
- Alert system

---

### 9. FEATURE DEMO - Analytics (20 seconds)

#### Scene 7: Analytics Dashboard
**Action**:
1. Navigate to Analytics page
2. Show charts and statistics
3. Highlight key metrics

**Script**:
> "The analytics dashboard provides insights into advisory trends, farmer engagement, and system performance."

**Highlight**:
- Advisory statistics
- Language distribution
- Engagement metrics

---

### 10. TECHNICAL HIGHLIGHTS (30 seconds)

**Visual**: Split screen or quick cuts showing:
1. AWS Console (Elastic Beanstalk)
2. S3 bucket for frontend
3. Code editor showing key files

**Script**:
> "Built entirely on AWS: Elastic Beanstalk for backend, S3 for frontend hosting, Bedrock for AI, and Polly for text-to-speech. The system is production-ready and scalable."

**On Screen Text**:
- ✅ AWS Bedrock (Nova Lite) for AI
- ✅ Sentinel Hub for satellite data
- ✅ OpenWeather API for forecasts
- ✅ Twilio for voice calls
- ✅ FastAPI + React architecture

---

### 11. IMPACT & FUTURE (25 seconds)

**Visual**: Show impact metrics or future roadmap
**Script**:
> "KrishiMitra bridges the digital divide by making advanced agricultural technology accessible to every farmer, regardless of language or literacy. Future plans include expanding to more languages, adding pest detection, and integrating with government schemes."

**On Screen Text**:
- 🎯 Current: Hindi & Telugu support
- 🚀 Future: 10+ Indian languages
- 🔬 Planned: Pest detection with computer vision
- 🤝 Goal: Reach 1M+ farmers

---

### 12. CLOSING (15 seconds)

**Visual**: 
- Show both URLs on screen
- GitHub repository link
- Contact information

**Script**:
> "KrishiMitra - Empowering farmers with AI. Try it live at the links shown. Thank you!"

**On Screen Text**:
- 🌐 Frontend: http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
- 🔧 Backend: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com
- 💻 GitHub: [Your GitHub URL]
- 📧 Contact: [Your Email]

---

## Recording Tips

### Before Recording
1. ✅ Clear browser cache and close unnecessary tabs
2. ✅ Set browser zoom to 100%
3. ✅ Hide bookmarks bar (Ctrl+Shift+B)
4. ✅ Use incognito/private mode for clean UI
5. ✅ Test all features work correctly
6. ✅ Have farmer phone ready for call demo
7. ✅ Prepare background music (optional)

### During Recording
1. **Speak clearly and confidently**
2. **Move mouse slowly and deliberately**
3. **Pause between sections** (easier to edit)
4. **Highlight important elements** with mouse
5. **Keep cursor movements smooth**
6. **Record in 1080p or higher**

### Screen Recording Settings (OBS Studio)
- Resolution: 1920x1080
- Frame Rate: 30 FPS
- Bitrate: 2500-5000 Kbps
- Audio: 192 Kbps

---

## Editing Checklist

### Video Editing
- [ ] Add title cards with transitions
- [ ] Add background music (low volume)
- [ ] Add text overlays for key points
- [ ] Add zoom effects for important UI elements
- [ ] Color grade for consistency
- [ ] Add fade in/out transitions
- [ ] Ensure audio levels are consistent

### Audio Editing
- [ ] Remove background noise
- [ ] Normalize audio levels
- [ ] Add subtle background music
- [ ] Ensure voice is clear and prominent

### Final Touches
- [ ] Add captions/subtitles (optional but recommended)
- [ ] Add your logo/branding
- [ ] Export in 1080p MP4
- [ ] Test on different devices
- [ ] Keep file size under 100MB if possible

---

## Alternative: Quick Demo (1-2 minutes)

If you need a shorter version:

1. **Opening** (10s): Problem + Solution
2. **Dashboard** (20s): Show farmer list and details
3. **Advisory** (30s): Generate and show advisory
4. **Voice Call** (30s): Demonstrate call feature
5. **Closing** (10s): Impact and links

---

## Pro Tips

### Make it Engaging
1. **Use storytelling**: "Meet Rajesh, a wheat farmer..."
2. **Show real data**: Use actual farmer information
3. **Demonstrate value**: Emphasize language support
4. **Keep it moving**: Don't linger too long on any screen
5. **End with impact**: Show how it helps farmers

### Common Mistakes to Avoid
- ❌ Too much technical jargon
- ❌ Long loading times (edit them out)
- ❌ Unclear audio
- ❌ Shaky cursor movements
- ❌ Too fast or too slow pacing
- ❌ Forgetting to show the voice call feature

### What Judges Look For
- ✅ Clear problem statement
- ✅ Innovative solution
- ✅ Working demo (not mockups)
- ✅ AWS integration
- ✅ Real-world impact
- ✅ Scalability potential
- ✅ Language accessibility

---

## Sample Script (Full Version)

```
[OPENING - 0:00-0:15]
"KrishiMitra - an AI-powered agricultural advisory system that helps farmers make data-driven decisions using satellite imagery, weather data, and AI-generated insights in their local language."

[PROBLEM - 0:15-0:35]
"Indian farmers face multiple challenges: unpredictable weather, crop diseases, and lack of timely information. Most agricultural advisories are in English, creating a language barrier for 80% of farmers who speak regional languages."

[SOLUTION - 0:35-0:55]
"KrishiMitra solves this by combining real-time satellite monitoring, weather forecasting, and AWS Bedrock AI to deliver personalized advisories in Hindi and Telugu through voice calls."

[DEMO START - 0:55-1:25]
"Let me show you how it works. Here's our dashboard showing registered farmers. Each farmer has their preferred language. Let's look at Rajesh Kumar, a wheat farmer from Maharashtra."

[ADVISORY - 1:25-2:25]
"Now, let's generate a personalized advisory. The system analyzes satellite data from Sentinel Hub, weather forecasts from OpenWeather, and uses AWS Bedrock to generate crop-specific recommendations in Hindi."

[VOICE CALL - 2:25-3:10]
"The most powerful feature - farmers receive these advisories via voice call. Watch as Rajesh receives his advisory in Hindi, making it accessible even for those who can't read."

[TECHNICAL - 3:10-3:40]
"Built entirely on AWS: Elastic Beanstalk for the backend, S3 for frontend hosting, Bedrock for AI, and Polly for text-to-speech. The system is production-ready and scalable."

[IMPACT - 3:40-4:05]
"KrishiMitra bridges the digital divide by making advanced agricultural technology accessible to every farmer, regardless of language or literacy."

[CLOSING - 4:05-4:20]
"Try it live at the links shown. KrishiMitra - Empowering farmers with AI. Thank you!"
```

---

## Video Export Settings

### For YouTube/Online
- Format: MP4 (H.264)
- Resolution: 1920x1080 (1080p)
- Frame Rate: 30 FPS
- Bitrate: 8-12 Mbps
- Audio: AAC, 192 Kbps

### For Submission
- Check hackathon requirements
- Usually: MP4, max 100MB or 5 minutes
- Include captions if required

---

## Backup Plan

If voice call doesn't work during recording:
1. Record the call separately beforehand
2. Edit it into the video
3. Or show a pre-recorded call demo
4. Always have a backup recording ready!

---

Good luck with your demo video! 🎥🌾
