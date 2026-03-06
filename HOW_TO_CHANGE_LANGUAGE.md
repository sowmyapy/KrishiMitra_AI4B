# How to Change Farmer's Language for Voice Calls

## Quick Steps

1. **Start the application** (if not already running):
   ```powershell
   .\start_all.ps1
   ```

2. **Open the web interface**:
   - Navigate to: http://localhost:3000

3. **Go to Farmers page**:
   - Click "Farmers" in the sidebar

4. **Select a farmer**:
   - Click on any farmer in the list to view their details

5. **Edit farmer information**:
   - Click the "Edit" button next to "Farmer Information"
   - A dialog will open

6. **Change the language**:
   - Select your desired language from the dropdown:
     - Hindi (हिन्दी)
     - English
     - Telugu (తెలుగు)
     - Tamil (தமிழ்)
     - Marathi (मराठी)
   - Click "Update"

7. **Generate a new advisory** (important!):
   - Click "Generate Advisory" button
   - Wait for the success message
   - This creates an advisory in the new language

8. **Test the voice call**:
   - Click "Make Voice Call" button
   - The farmer will receive a call in their newly selected language

## Important Notes

- **You must generate a new advisory** after changing the language for the voice call to use the new language
- The advisory text is generated in the farmer's language
- The voice call reads the advisory using the correct language's text-to-speech
- Old advisories remain in their original language

## Example: Changing to Telugu

1. Edit farmer → Select "Telugu (తెలుగు)"
2. Click Update
3. Click "Generate Advisory"
4. Click "Make Voice Call"
5. Farmer receives call in Telugu

## Troubleshooting

### Voice call still in wrong language?
- Make sure you generated a NEW advisory after changing the language
- Old advisories are in the old language
- Check that the farmer's language was actually updated (refresh the page)

### Can't update farmer?
- Make sure the backend is running
- Check backend logs for errors
- Verify ngrok is running if testing voice calls

### No advisory generated?
- Make sure the farmer has at least one plot
- Check backend logs for errors
- Verify API keys are configured in .env file

## Technical Details

The language change affects:
1. **Advisory text generation** - Generated in farmer's language
2. **Voice call greeting** - "नमस्ते" (Hindi) vs "నమస్కారం" (Telugu)
3. **Advisory delivery** - Read in farmer's language
4. **Replay prompt** - Instructions in farmer's language
5. **Goodbye message** - Farewell in farmer's language

All of this happens automatically once you update the farmer's language preference!
