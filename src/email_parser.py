import base64
from email.utils import parsedate_to_datetime

def get_body(payload):
    if "data" in payload["body"]:
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

    return ""


def parse_email(msg):
    headers = msg["payload"]["headers"]
    data = {}

    for h in headers:
        if h["name"] == "From":
            data["from"] = h["value"]
        if h["name"] == "Subject":
            data["subject"] = h["value"]
        if h["name"] == "Date":
            data["date"] = parsedate_to_datetime(h["value"]).strftime("%Y-%m-%d %H:%M:%S")

    data["body"] = get_body(msg["payload"])
    return data
