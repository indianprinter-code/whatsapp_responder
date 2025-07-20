# Meta WhatsApp Business API Setup Guide

## Step 1: Meta Developer Account Setup

1. **Visit** https://developers.facebook.com/
2. **Log in** with your Facebook account
3. **Create a new app** or use existing one
4. **Select "Business"** as the app type

## Step 2: WhatsApp Business API Setup

1. **In your app dashboard:**
   - Click "Add Product"
   - Find "WhatsApp" and click "Set Up"
   - Choose "Business" as the use case

2. **Add a Phone Number:**
   - Go to WhatsApp > Getting Started
   - Click "Add phone number"
   - Follow the verification process
   - **Note down your Phone Number ID**

3. **Generate Access Token:**
   - Go to WhatsApp > API Setup
   - Click "Generate token"
   - **Copy your Access Token**

4. **Create Verify Token:**
   - Create a custom token (e.g., "my_whatsapp_verify_token_123")
   - **Note down your Verify Token**

## Step 3: Environment Variables

Create a `.env` file with your credentials:

```env
SPREADSHEET_ID=1o31IoLhW67QFG9XAxm3CTpTK6TATe0A7c1lYaIoiLdw
SHEET_NAME=Sheet1
WHATSAPP_TOKEN=your_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_VERIFY_TOKEN=your_verify_token_here
```

## Step 4: Deploy Your App

### Option A: Using ngrok (for testing)
1. **Install ngrok:** https://ngrok.com/
2. **Run your Flask app:** `python app.py`
3. **In another terminal:** `ngrok http 5000`
4. **Copy the ngrok URL** (e.g., https://abc123.ngrok.io)

### Option B: Using a hosting service
- **Heroku, Railway, or similar**
- Deploy your app and get the public URL

## Step 5: Configure Webhook

1. **In Meta Developer Console:**
   - Go to WhatsApp > Configuration
   - Click "Edit" on Webhook
   - **Webhook URL:** `https://your-domain.com/webhook`
   - **Verify Token:** Your custom verify token
   - **Subscribe to:** messages

2. **Test the webhook:**
   - Send a message to your WhatsApp number
   - Check if you receive a response

## Step 6: Test Your Bot

1. **Visit** `http://localhost:5000/test_webhook` in your browser
2. **Send a message** to your WhatsApp number
3. **Check the response**

## Troubleshooting

### Common Issues:
1. **Webhook verification fails:** Check your verify token
2. **Messages not received:** Ensure webhook URL is accessible
3. **Authentication errors:** Verify your access token
4. **Phone number not verified:** Complete the verification process

### Support Resources:
- Meta Developer Documentation: https://developers.facebook.com/docs/whatsapp
- WhatsApp Business API Guide: https://developers.facebook.com/docs/whatsapp/cloud-api

## Next Steps

Once setup is complete, you can:
1. **Add order management features**
2. **Implement document sharing**
3. **Add interactive buttons**
4. **Create template messages** 