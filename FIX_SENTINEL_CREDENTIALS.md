# Fix Sentinel Hub Credentials

Your `.env` file currently has placeholder values. You need to replace them with actual credentials.

## Current Issue

```
SENTINEL_HUB_CLIENT_ID=your_client_id
SENTINEL_HUB_CLIENT_SECRET=your_client_secret
```

These are placeholders, not real credentials!

## How to Get Real Credentials

### Step 1: Go to Sentinel Hub Dashboard

Open: https://apps.sentinel-hub.com/dashboard/

### Step 2: Find Your Credentials

1. Click on **"User Settings"** (top right, your profile icon)
2. Go to **"OAuth clients"** tab
3. You should see your OAuth client listed

### Step 3: Copy Your Credentials

You'll see:
- **Client ID**: A long string like `12345678-1234-1234-1234-123456789abc`
- **Client Secret**: Click "Show" to reveal it, looks like `abcdefgh-abcd-abcd-abcd-abcdefghijkl`

### Step 4: Update Your .env File

Open `.env` file and replace the placeholders:

```env
# Replace these lines:
SENTINEL_HUB_CLIENT_ID=your_client_id
SENTINEL_HUB_CLIENT_SECRET=your_client_secret

# With your actual credentials:
SENTINEL_HUB_CLIENT_ID=12345678-1234-1234-1234-123456789abc
SENTINEL_HUB_CLIENT_SECRET=abcdefgh-abcd-abcd-abcd-abcdefghijkl
```

## If You Don't Have an Account Yet

### Create Free Account (5 minutes)

1. Go to: https://www.sentinel-hub.com/
2. Click **"Try for free"** or **"Sign up"**
3. Fill in your details:
   - Email
   - Password
   - Name
   - Organization (can be "Personal" or "Testing")
4. Verify your email
5. Log in to dashboard

### Create OAuth Client

After logging in:

1. Go to **User Settings** → **OAuth clients**
2. Click **"Create new OAuth client"**
3. Give it a name (e.g., "KrishiMitra")
4. Click **"Create"**
5. Copy the **Client ID** and **Client Secret**

## After Updating .env

Save the file and test again:

```powershell
python scripts/test_sentinel.py
```

## Still Having Issues?

### Check Processing Units

Free tier includes:
- 30,000 processing units per month
- Resets monthly

Check your quota at: https://apps.sentinel-hub.com/dashboard/#/account/settings

### Wait for Activation

If you just created the account:
- Wait 5-10 minutes for activation
- Try the test again

### Verify Credentials Format

Make sure:
- No quotes around the values
- No extra spaces
- Full credential string copied
- Both Client ID and Secret are on separate lines

## Example .env Format

```env
# Correct format (no quotes, no spaces)
SENTINEL_HUB_CLIENT_ID=12345678-1234-1234-1234-123456789abc
SENTINEL_HUB_CLIENT_SECRET=abcdefgh-abcd-abcd-abcd-abcdefghijkl

# Wrong formats:
SENTINEL_HUB_CLIENT_ID="12345678-1234-1234-1234-123456789abc"  # ✗ Has quotes
SENTINEL_HUB_CLIENT_ID = 12345678-1234-1234-1234-123456789abc  # ✗ Extra spaces
SENTINEL_HUB_CLIENT_ID=your_client_id  # ✗ Still placeholder
```

## Need Help?

If you're stuck:
1. Double-check you're logged into Sentinel Hub dashboard
2. Verify the OAuth client exists in User Settings
3. Make sure you copied the entire credential string
4. Check there are no hidden characters or line breaks
