import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# --- CONFIG ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# You will need to create a service account and download the JSON key file
# from Google Cloud Console and save it as 'service-account-key.json'
SERVICE_ACCOUNT_FILE = 'service-account-key.json'

def authenticate_google_sheets():
    """Authenticates with the Google Sheets API using a service account."""
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def get_sheet_data(spreadsheet_id, sheet_name):
    """Gets all data from a specific sheet."""
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=sheet_name).execute()
    values = result.get('values', [])
    return values

def update_sheet_data(spreadsheet_id, range_name, values):
    """Updates a range of cells in a specific sheet."""
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    return result 