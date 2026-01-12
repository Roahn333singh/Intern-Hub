# Deployment Guide - Render

This guide will help you deploy InternHub AI to Render.com.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Render account (sign up at https://render.com)
4. Your Gemini API key

## Step-by-Step Deployment

### Step 1: Push Code to GitHub

1. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - InternHub AI"
   ```

2. Create a new repository on GitHub

3. Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/internhub-ai.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Create Render Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository: `internhub-ai`

### Step 3: Configure Build Settings

Render will auto-detect Python, but verify these settings:

- **Name**: `internhub-ai` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 4: Add Environment Variables

In the Render dashboard, go to **Environment** section and add:

1. **GEMINI_API_KEY**
   - Key: `GEMINI_API_KEY`
   - Value: Your Gemini API key (get from https://makersuite.google.com/app/apikey)

2. **GEMINI_MODEL** (Optional)
   - Key: `GEMINI_MODEL`
   - Value: `gemini-2.5-flash` (or your preferred model)

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying your application
3. Wait for the build to complete (usually 2-5 minutes)
4. Your app will be live at: `https://your-app-name.onrender.com`

## Alternative: Using render.yaml

If you've included `render.yaml` in your repository:

1. Go to Render Dashboard
2. Click **"New +"** → **"Blueprint"**
3. Select your repository
4. Render will auto-detect `render.yaml` and use those settings
5. Add your `GEMINI_API_KEY` in the environment variables section
6. Deploy!

## Post-Deployment

### Verify Deployment

1. Visit your app URL: `https://your-app-name.onrender.com`
2. Test the health endpoint: `https://your-app-name.onrender.com/health`
3. Try the web UI: `https://your-app-name.onrender.com/`
4. Check API docs: `https://your-app-name.onrender.com/docs`

### Important Notes

- **Free Tier Limitations**: 
  - Render free tier services spin down after 15 minutes of inactivity
  - First request after spin-down may take 30-60 seconds
  - Consider upgrading for production use

- **Environment Variables**:
  - Never commit `.env` file to GitHub
  - Always set environment variables in Render dashboard
  - `.env` is already in `.gitignore`

- **Processing Time**:
  - AI processing takes 10-30 seconds
  - Render free tier has request timeout limits
  - If requests timeout, consider upgrading or optimizing prompts

## Troubleshooting

### Build Fails

- Check that `requirements.txt` has all dependencies
- Verify Python version compatibility
- Check build logs in Render dashboard

### App Crashes on Start

- Verify `GEMINI_API_KEY` is set correctly
- Check that port is using `$PORT` environment variable
- Review logs in Render dashboard

### API Not Working

- Verify Gemini API key is valid
- Check API quota limits
- Review error logs in Render dashboard

### Timeout Issues

- Free tier has request timeout limits
- Consider optimizing prompts for faster responses
- Upgrade to paid plan for longer timeouts

## Updating Your Deployment

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```

2. Render will automatically detect changes and redeploy
3. Monitor the deployment in Render dashboard

## Custom Domain (Optional)

1. Go to your service settings in Render
2. Click **"Custom Domains"**
3. Add your domain
4. Follow DNS configuration instructions

## Monitoring

- View logs: Render Dashboard → Your Service → Logs
- Monitor metrics: Render Dashboard → Your Service → Metrics
- Set up alerts: Render Dashboard → Your Service → Alerts

## Cost Estimation

- **Free Tier**: $0/month (with limitations)
- **Starter Plan**: $7/month (better performance, no spin-down)
- **Standard Plan**: $25/month (production-ready)

---

**Your deployed app will be available at:**
`https://your-app-name.onrender.com`

**API Documentation:**
`https://your-app-name.onrender.com/docs`

**Health Check:**
`https://your-app-name.onrender.com/health`

