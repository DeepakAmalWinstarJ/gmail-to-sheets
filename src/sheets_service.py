import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SHEET_ID

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheets_service():
    creds = None

    if os.path.exists("credentials/sheets_token.pickle"):
        with open("credentials/sheets_token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("credentials/sheets_token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("sheets", "v4", credentials=creds)


def append_rows(rows):
    service = get_sheets_service()
    body = {"values": rows}

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range="Sheet1!A:D",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
