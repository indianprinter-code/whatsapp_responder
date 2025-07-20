import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# --- CONFIG ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_google_sheets():
    """Authenticates with the Google Sheets API using service account credentials from environment."""
    try:
        # Try to get service account credentials from environment variable
        service_account_info = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        if service_account_info:
            # Parse the JSON string from environment variable
            service_account_dict = json.loads(service_account_info)
            creds = Credentials.from_service_account_info(
                service_account_dict, scopes=SCOPES)
            return creds
        else:
            # Fallback: try to read from file (for local development)
            SERVICE_ACCOUNT_FILE = 'service-account-key.json'
            if os.path.exists(SERVICE_ACCOUNT_FILE):
                creds = Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
                return creds
            else:
                raise Exception("No Google service account credentials found. Please set GOOGLE_SERVICE_ACCOUNT_JSON environment variable.")
    except Exception as e:
        print(f"Authentication error: {e}")
        # Return a mock response for testing
        return None

def get_sheet_data(spreadsheet_id, sheet_name):
    """Gets all data from a specific sheet."""
    try:
        creds = authenticate_google_sheets()
        if not creds:
            # Return mock data for testing
            return [
                ["Question", "Answer"],
                ["hello", "Hi! How can I help you today?"],
                ["order status", "Please provide your order number to check status."],
                ["urgent", "I'll mark your order as urgent. Please provide order details."]
            ]
        
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=sheet_name).execute()
        values = result.get('values', [])
        return values
    except Exception as e:
        print(f"Error getting sheet data: {e}")
        # Return mock data for testing
        return [
            ["Question", "Answer"],
            ["hello", "Hi! How can I help you today?"],
            ["order status", "Please provide your order number to check status."],
            ["urgent", "I'll mark your order as urgent. Please provide order details."]
        ]

def update_sheet_data(spreadsheet_id, range_name, values):
    """Updates a range of cells in a specific sheet."""
    try:
        creds = authenticate_google_sheets()
        if not creds:
            return {"message": "Mock update - no credentials available"}
        
        service = build('sheets', 'v4', credentials=creds)
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='RAW', body=body).execute()
        return result
    except Exception as e:
        print(f"Error updating sheet data: {e}")
        return {"message": f"Error updating sheet: {e}"} 