# Railway Deployment Guide

## Step 1: Create GitHub Repository

1. **Go to** https://github.com/
2. **Click "New repository"**
3. **Name it:** `whatsapp-responder`
4. **Make it Public** (Railway needs access)
5. **Click "Create repository"**

## Step 2: Upload Your Code to GitHub

### Option A: Using GitHub Desktop
1. **Download GitHub Desktop** from https://desktop.github.com/
2. **Clone your repository**
3. **Copy your files** to the repository folder
4. **Commit and push**

### Option B: Using Git Commands
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/whatsapp-responder.git
git push -u origin main
```

## Step 3: Deploy to Railway

1. **Go back to Railway** (https://railway.app/)
2. **Click "Deploy from GitHub repo"**
3. **Select your repository:** `whatsapp-responder`
4. **Railway will automatically detect Python and deploy**

## Step 4: Get Your Webhook URL

Once deployed, Railway will give you a URL like:
`https://your-app-name.railway.app`

Your webhook URL will be:
`https://your-app-name.railway.app/webhook`

## Step 5: Configure Meta Webhook

1. **Go back to Meta Developer Console**
2. **Update webhook URL** to your Railway URL
3. **Verify token:** `my_whatsapp_verify_token_123`
4. **Click "Verify and save"**

## Step 6: Get Meta Credentials

1. **Phone Number ID** (from phone numbers section)
2. **Access Token** (from permanent token section)
3. **Update environment variables in Railway**

## Troubleshooting

- **If deployment fails:** Check that all files are in the repository
- **If webhook fails:** Make sure the URL is accessible
- **If credentials don't work:** Verify they're correct in Railway environment variables 