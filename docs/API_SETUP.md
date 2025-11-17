# 🔑 API Setup Guide

This guide will help you get all the API keys needed for YuvaSaarthi.

**⏱️ Total Time Required: ~20 minutes**

---

## 1. Groq API (Required) ✅

**Purpose:** Powers the AI brain of the chatbot
**Cost:** FREE
**Time:** 2 minutes

### Steps:

1. **Visit Groq Console**
   - Go to: https://console.groq.com

2. **Sign Up / Login**
   - Click "Sign In" or "Sign Up"
   - Use Google/GitHub or email

3. **Create API Key**
   - Go to "API Keys" section
   - Click "Create API Key"
   - Give it a name: "YuvaSaarthi"
   - Copy the API key (starts with `gsk_...`)

4. **Add to .env file**
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

**Note:** Groq offers free tier with:
- 30 requests/minute
- Plenty for demo and small-scale use

---

## 2. Bhashini API (Optional) ⚠️

**Purpose:** Translation between Hindi, English, and Rajasthani
**Cost:** FREE
**Time:** 10 minutes

### Steps:

1. **Visit Bhashini Portal**
   - Go to: https://bhashini.gov.in/ulca

2. **Register**
   - Click "User Register"
   - Fill in details:
     - Name
     - Email
     - Phone Number
     - Organization: Your College Name
     - Purpose: Educational/Research
   - Submit

3. **Verify Email**
   - Check your email for verification link
   - Click to verify

4. **Login**
   - Go to: https://bhashini.gov.in/ulca/user/login
   - Login with credentials

5. **Get API Credentials**
   - Go to "Profile" or "API Keys" section
   - Note down:
     - User ID
     - API Key
     - Pipeline ID (for translation)

6. **Add to .env file**
   ```env
   BHASHINI_USER_ID=your_user_id_here
   BHASHINI_API_KEY=your_api_key_here
   BHASHINI_PIPELINE_ID=your_pipeline_id_here
   ```

**Note:** If Bhashini is not configured, the chatbot will still work but won't translate between languages.

---

## 3. YouTube Data API (Optional) ⚠️

**Purpose:** Educational video recommendations
**Cost:** FREE (10,000 requests/day)
**Time:** 5 minutes

### Steps:

1. **Visit Google Cloud Console**
   - Go to: https://console.cloud.google.com

2. **Create Project**
   - Click "Select Project" → "New Project"
   - Name: "YuvaSaarthi"
   - Click "Create"

3. **Enable YouTube Data API v3**
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click on it
   - Click "Enable"

4. **Create Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key

5. **Restrict API Key (Optional but recommended)**
   - Click on your API key
   - Under "API restrictions":
     - Select "Restrict key"
     - Check "YouTube Data API v3"
   - Save

6. **Add to .env file**
   ```env
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

**Note:** Without YouTube API, the chatbot won't show video recommendations but will still answer questions.

---

## 4. Telegram Bot Token (Optional) ⚠️

**Purpose:** Run chatbot on Telegram
**Cost:** FREE
**Time:** 2 minutes

### Steps:

1. **Open Telegram**
   - If you don't have Telegram, download it: https://telegram.org

2. **Find BotFather**
   - Search for `@BotFather` in Telegram
   - Start a chat with it

3. **Create New Bot**
   - Send command: `/newbot`
   - BotFather will ask for bot name
   - Enter: `YuvaSaarthi Educational Bot` (or any name you like)

4. **Set Username**
   - BotFather will ask for username
   - Enter: `yuvasaarthi_yourname_bot` (must end with `bot`)
   - Example: `yuvasaarthi_raj_bot`

5. **Get Token**
   - BotFather will give you a token
   - It looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - Copy this token

6. **Add to .env file**
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_token_here
   ```

**Note:** Only needed if you want to use Telegram interface. Web interface works without it.

---

## 📝 Complete .env File Example

After getting all keys, your `.env` file should look like:

```env
# LLM Configuration (Required)
GROQ_API_KEY=gsk_abc123xyz789...

# Translation API (Optional)
BHASHINI_USER_ID=user_12345
BHASHINI_API_KEY=bhashini_key_abc123
BHASHINI_PIPELINE_ID=pipeline_xyz

# YouTube API (Optional)
YOUTUBE_API_KEY=AIzaSyA...

# Telegram Bot (Optional - only if using Telegram)
TELEGRAM_BOT_TOKEN=123456789:ABCdef...

# Bot Configuration
BOT_NAME=YuvaSaarthi
BOT_PERSONALITY=mix
DEFAULT_LANGUAGE=hi

# Department Details
DEPARTMENT_NAME=Department of Technical Education
ORGANIZATION=Government of Rajasthan
LOCATION=Rajasthan, India
WEBSITE=https://dte.rajasthan.gov.in
```

---

## ✅ Verify Your Setup

After adding API keys, test them:

```bash
python -m utils.config
```

This will show which APIs are configured correctly.

---

## 🔒 Security Tips

1. **Never share your API keys publicly**
2. **Never commit .env file to Git**
3. **Keep backup of your keys in a safe place**
4. **Regenerate keys if compromised**
5. **Set usage limits on cloud platforms**

---

## ❓ FAQ

### Q: Which APIs are absolutely required?
**A:** Only Groq API is required. Others enhance functionality.

### Q: What if I can't get Bhashini API?
**A:** The chatbot will still work. It just won't translate between languages. Users can still use the bot in any language, just responses won't be translated.

### Q: YouTube API quota exceeded?
**A:** Free tier gives 10,000 requests/day. For demo, this is more than enough. If exceeded, video recommendations will be disabled temporarily.

### Q: How do I know if my keys are working?
**A:** Run health check:
```bash
python -m backend.chatbot_engine
```

### Q: Can I use this without any API keys?
**A:** No, at minimum you need Groq API for the LLM to work.

---

## 🆘 Troubleshooting

### "Invalid API Key" Error
- Double-check you copied the entire key
- Make sure there are no extra spaces
- Check if key is active on the provider's dashboard

### "Rate Limit Exceeded"
- Wait a few minutes
- Check usage on provider's dashboard
- For Groq: 30 requests/minute limit

### "Authentication Failed"
- Verify email is confirmed
- Check if account is active
- Try regenerating the key

---

## 📞 Need Help?

- **Groq:** https://console.groq.com/docs
- **Bhashini:** https://bhashini.gov.in/ulca/user/docs
- **YouTube API:** https://developers.google.com/youtube/v3
- **Telegram Bots:** https://core.telegram.org/bots

---

**Next:** [Usage Guide](USAGE.md)
