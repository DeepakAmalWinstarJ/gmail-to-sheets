import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gmail_service import get_gmail_service
from sheets_service import append_rows
from email_parser import parse_email
from config import STATE_FILE

def load_processed():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_processed(msg_id):
    with open(STATE_FILE, "a") as f:
        f.write(msg_id + "\n")

def main():
    service = get_gmail_service()
    processed = load_processed()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    messages = results.get("messages", [])

    rows = []

    for m in messages:
        msg_id = m["id"]

        if msg_id in processed:
            continue

        msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        data = parse_email(msg)

        rows.append([
            data["from"],
            data["subject"],
            data["date"],
            data["body"]
        ])

        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        save_processed(msg_id)

    if rows:
        append_rows(rows)
        print("Emails added to Google Sheet.")
    else:
        print("No new emails.")

if __name__ == "__main__":
    main()
