from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
import json
from google_sheets import get_sheet_data

load_dotenv()

app = Flask(__name__)

# --- CONFIG ---
# You'll need to add your Spreadsheet ID and the name of the sheet
# you want to use as a database.
# You can add these to a .env file or set them as environment variables.
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "1o31IoLhW67QFG9XAxm3CTpTK6TATe0A7c1lYaIoiLdw")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")

# WhatsApp API Configuration - Choose your provider
WHATSAPP_PROVIDER = "META"  # Options: "META" or "TWILIO"

# Meta WhatsApp Business API Configuration
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "YOUR_WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "my_whatsapp_token")

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "+14155238886")


@app.route("/")
def hello():
    return "Hello, this is your WhatsApp Responder!"

@app.route("/test")
def test():
    """Simple test endpoint to verify the app is running."""
    return jsonify({
        "status": "success",
        "message": "WhatsApp Responder is running!",
        "spreadsheet_id": SPREADSHEET_ID,
        "sheet_name": SHEET_NAME,
        "whatsapp_provider": WHATSAPP_PROVIDER
    })

@app.route("/switch_provider/<provider>")
def switch_provider(provider):
    """Switch between META and TWILIO providers."""
    global WHATSAPP_PROVIDER
    if provider.upper() in ["META", "TWILIO"]:
        WHATSAPP_PROVIDER = provider.upper()
        return jsonify({
            "status": "success",
            "message": f"Switched to {WHATSAPP_PROVIDER}",
            "current_provider": WHATSAPP_PROVIDER
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid provider. Use 'META' or 'TWILIO'"
        }), 400

@app.route("/sheet_data")
def sheet_data():
    """Fetches and displays data from the Google Sheet."""
    try:
        # Use simple range format since sheet name has no spaces
        range_name = f"{SHEET_NAME}!A:Z"
        data = get_sheet_data(SPREADSHEET_ID, range_name)
        return jsonify({
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/list_sheets")
def list_sheets():
    """Lists all available sheets in the Google Spreadsheet."""
    try:
        from google_sheets import authenticate_google_sheets
        from googleapiclient.discovery import build
        
        creds = authenticate_google_sheets()
        service = build('sheets', 'v4', credentials=creds)
        
        # Get spreadsheet metadata
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=SPREADSHEET_ID
        ).execute()
        
        sheets = []
        for sheet in spreadsheet['sheets']:
            sheets.append(sheet['properties']['title'])
        
        return jsonify({
            "status": "success",
            "sheets": sheets,
            "spreadsheet_title": spreadsheet['properties']['title']
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def send_whatsapp_message(phone_number, message):
    """Send a WhatsApp message using the selected provider."""
    if WHATSAPP_PROVIDER == "META":
        return send_whatsapp_message_meta(phone_number, message)
    elif WHATSAPP_PROVIDER == "TWILIO":
        return send_whatsapp_message_twilio(phone_number, message)
    else:
        print(f"Unknown provider: {WHATSAPP_PROVIDER}")
        return None

def send_whatsapp_message_meta(phone_number, message):
    """Send a WhatsApp message using Meta's API."""
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def send_whatsapp_message_twilio(phone_number, message):
    """Send a WhatsApp message using Twilio."""
    from twilio.rest import Client
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            body=message,
            to=f'whatsapp:{phone_number}'
        )
        print(f"Message sent successfully to {phone_number}")
        return message.sid
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    """WhatsApp webhook - supports both Meta and Twilio."""
    print(f"Webhook called with method: {request.method}")
    print(f"Current provider: {WHATSAPP_PROVIDER}")
    print(f"Request args: {request.args}")
    
    # Handle Meta webhook verification for GET requests
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        # If this is a Meta webhook verification
        if mode == 'subscribe' and token == WHATSAPP_VERIFY_TOKEN and challenge:
            print(f"Meta webhook verification successful, returning challenge: {challenge}")
            return challenge  # Return just the challenge value
        
        # Otherwise return debug info
        return jsonify({
            "status": "webhook_working",
            "method": "GET",
            "provider": WHATSAPP_PROVIDER,
            "args": dict(request.args)
        })
    
    if WHATSAPP_PROVIDER == "META":
        return webhook_meta()
    elif WHATSAPP_PROVIDER == "TWILIO":
        return webhook_twilio()
    else:
        print(f"Unknown provider: {WHATSAPP_PROVIDER}")
        return 'Unknown provider', 400

def webhook_meta():
    """Meta WhatsApp Business API webhook."""
    # GET requests are handled in the main webhook function
    if request.method == 'GET':
        return 'Method not allowed', 405
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Extract message data
            if 'entry' in data and len(data['entry']) > 0:
                entry = data['entry'][0]
                if 'changes' in entry and len(entry['changes']) > 0:
                    change = entry['changes'][0]
                    if 'value' in change and 'messages' in change['value']:
                        message = change['value']['messages'][0]
                        
                        # Get message details
                        phone_number = message['from']
                        message_text = message['text']['body'].lower().strip()
                        
                        # Process message and send response
                        process_message(phone_number, message_text)
            
            return 'OK', 200
            
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return 'Error', 500

def webhook_twilio():
    """Twilio WhatsApp webhook."""
    if request.method == 'POST':
        try:
            # Extract message data from Twilio
            from_number = request.form.get('From')
            message_text = request.form.get('Body', '').lower().strip()
            
            if from_number and message_text:
                # Process message and send response
                process_message(from_number, message_text)
            
            return 'OK', 200
            
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return 'Error', 500
    
    return 'Method not allowed', 405

def process_message(phone_number, message_text):
    """Process incoming message and send response."""
    # Get Q&A data from Google Sheets
    range_name = f"{SHEET_NAME}!A:Z"
    sheet_data = get_sheet_data(SPREADSHEET_ID, range_name)
    
    # Find matching answer
    answer = "I'm sorry, I don't have an answer for that question. Please contact our support team."
    
    for row in sheet_data[1:]:  # Skip header row
        if len(row) >= 2:
            question = row[0].lower().strip()
            if message_text in question or question in message_text:
                answer = row[1]
                break
    
    # Send response
    send_whatsapp_message(phone_number, answer)

@app.route("/webhook_test")
def webhook_test():
    """Simple test to verify webhook endpoint is accessible."""
    return jsonify({
        "status": "success",
        "message": "Webhook endpoint is accessible",
        "verify_token": WHATSAPP_VERIFY_TOKEN,
        "provider": WHATSAPP_PROVIDER
    })

@app.route("/test_webhook")
def test_webhook():
    """Test the webhook functionality locally."""
    try:
        # Simulate a WhatsApp message
        test_message = "hello"
        
        # Get Q&A data from Google Sheets
        range_name = f"{SHEET_NAME}!A:Z"
        sheet_data = get_sheet_data(SPREADSHEET_ID, range_name)
        
        # Find matching answer
        answer = "I'm sorry, I don't have an answer for that question. Please contact our support team."
        
        for row in sheet_data[1:]:  # Skip header row
            if len(row) >= 2:
                question = row[0].lower().strip()
                if test_message in question or question in test_message:
                    answer = row[1]
                    break
        
        return jsonify({
            "status": "success",
            "test_message": test_message,
            "response": answer
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000)) 