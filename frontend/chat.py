import streamlit as st
import google.generativeai as genai
import requests
import os
from datetime import datetime, timedelta
import re

# Load Gemini API key (use os.getenv for security in production)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")  # or "gemini-pro" if that's working

# Function to detect greetings
def is_greeting(message):
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good evening']
    return any(word in message.lower() for word in greetings)

# Function to extract booking info
def extract_booking_info(user_message):
    prompt = f"""
You are a smart calendar booking assistant. Extract booking details from the user message if it contains one.

User Message: "{user_message}"

Return only this format if booking info is found:
summary: <short title of event>
date: <YYYY-MM-DD>
time: <HH:MM> (24-hour format)

If it's just a greeting or chat (not a booking), return:
chat: <your friendly response>
"""
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Check for chat mode
    if text.lower().startswith("chat:"):
        return {"chat": text.split("chat:")[1].strip()}

    # Try to extract booking
    match = re.search(r'summary:\s*(.*)\ndate:\s*(.*)\ntime:\s*(.*)', text)
    if match:
        return {
            "summary": match.group(1).strip(),
            "date": match.group(2).strip(),
            "time": match.group(3).strip()
        }

    return "error"

# Function to call backend FastAPI safely
def book_event(info):
    try:
        res = requests.post("http://localhost:8000/book", json=info)
        if res.ok:
            return True, res.json()
        else:
            return False, res.text
    except Exception as e:
        return False, str(e)

# Streamlit Chat UI
st.title("📅 Gemini Smart Appointment Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("What appointment would you like to book or ask me?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking..."):
        info = extract_booking_info(user_input)
        print("Gemini Response:", info)

        if isinstance(info, dict) and "chat" in info:
            reply = info["chat"]
        elif info == "error":
            reply = "❌ Sorry, I couldn't understand your request."
        else:
            success, result = book_event(info)
            if success:
                reply = f"✅ Booked *{info['summary']}* on {info['date']} at {info['time']}."
            else:
                reply = f"❌ Booking failed. Reason: {result}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

# Show messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
