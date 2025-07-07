from fastapi import FastAPI, Request
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'
CALENDAR_ID = 'lokesi5678@gmail.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

class BookingRequest(BaseModel):
    summary: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM (24h)

@app.post("/book")
def book_calendar_event(req: BookingRequest):
    start_time = f"{req.date}T{req.time}:00"
    end_time = (datetime.datetime.fromisoformat(start_time) + datetime.timedelta(hours=1)).isoformat()

    event = {
        'summary': req.summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }

    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return {"status": "success", "start": start_time}
