# Gmail to Google Sheets Automation

## 📌 Overview
This project reads unread emails from Gmail and logs them into a Google Sheet using Google APIs.

## 🧠 Architecture
Gmail API → Python → Email Parser → Google Sheets API

## ⚙️ Technologies
- Python 3
- Gmail API
- Google Sheets API
- OAuth 2.0

## 🔄 How it works
1. Authenticate with Gmail and Google Sheets
2. Fetch unread emails
3. Extract sender, subject, date, body
4. Append to Google Sheet
5. Mark email as read
6. Save processed message IDs to avoid duplicates

## 🧾 State Management
Processed Gmail message IDs are stored in `processed_emails.txt` so reruns do not duplicate rows.

## 🔐 Security
OAuth tokens and credentials.json are excluded using `.gitignore`.

## 👤 Author
Deepak Amal Winstar J
