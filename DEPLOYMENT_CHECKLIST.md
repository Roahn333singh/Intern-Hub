# Render Deployment Checklist

Use this checklist to ensure your deployment goes smoothly.

## Pre-Deployment Checklist

- [ ] Code is pushed to GitHub repository
- [ ] `.env` file is in `.gitignore` (should not be committed)
- [ ] All dependencies are in `requirements.txt`
- [ ] `render.yaml` file is created (optional but helpful)
- [ ] You have your Gemini API key ready

## Render Setup Steps

### 1. Create Render Account
- [ ] Sign up at https://render.com
- [ ] Verify your email

### 2. Connect GitHub
- [ ] Connect your GitHub account in Render dashboard
- [ ] Grant access to your repository

### 3. Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Select your repository: `internhub-ai`
- [ ] Choose branch: `main` (or your default branch)

### 4. Configure Settings

**Basic Settings:**
- [ ] Name: `internhub-ai` (or your choice)
- [ ] Environment: `Python 3`
- [ ] Region: Choose closest to users

**Build & Deploy:**
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 5. Environment Variables
- [ ] Add `GEMINI_API_KEY` = your API key
- [ ] Add `GEMINI_MODEL` = `gemini-2.5-flash` (optional)

### 6. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (2-5 minutes)
- [ ] Check build logs for any errors

## Post-Deployment Verification

- [ ] Visit your app URL: `https://your-app-name.onrender.com`
- [ ] Test health endpoint: `/health` should return `{"status": "healthy"}`
- [ ] Test web UI: `/` should show the form
- [ ] Test API docs: `/docs` should show Swagger UI
- [ ] Test an API endpoint (e.g., `/api/match-summary`)

## Quick Test Commands

After deployment, test these URLs:

```bash
# Health check
curl https://your-app-name.onrender.com/health

# API docs
open https://your-app-name.onrender.com/docs

# Test endpoint (replace with your data)
curl -X POST https://your-app-name.onrender.com/api/match-summary \
  -H "Content-Type: application/json" \
  -d '{"user_profile": {"skills": ["Python"], "interests": ["Web Dev"]}, "internship": {"title": "Test", "description": "Test", "requirements": ["Python"]}}'
```

## Common Issues & Solutions

### Issue: Build fails
- **Solution**: Check `requirements.txt` has all packages
- **Solution**: Verify Python version compatibility

### Issue: App crashes on start
- **Solution**: Check `GEMINI_API_KEY` is set
- **Solution**: Verify start command uses `$PORT`

### Issue: 502 Bad Gateway
- **Solution**: Check logs in Render dashboard
- **Solution**: Verify app is listening on correct port

### Issue: Timeout errors
- **Solution**: Free tier has timeout limits
- **Solution**: Consider upgrading or optimizing prompts

## Your Deployment URLs

After successful deployment:

- **Web UI**: `https://your-app-name.onrender.com/`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **Health Check**: `https://your-app-name.onrender.com/health`
- **API Base**: `https://your-app-name.onrender.com/api/`

## Next Steps After Deployment

1. Test all 5 endpoints
2. Share the live URL in your submission
3. Update README with live deployment link
4. Monitor logs for any issues

---

**Ready to deploy?** Follow the steps in `DEPLOYMENT.md` for detailed instructions!

