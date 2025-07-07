# 🤖 Gemini-Powered AI Booking Agent

This is a smart, conversational AI assistant that books Google Calendar appointments using natural language. It uses Google Gemini for understanding user intent and FastAPI + Google Calendar API for event creation.

> 🌐 Live Demo: https://ai-booking-agent-2.onrender.com

---

## 🚀 Features

- 🧠 Natural language understanding via **Gemini Pro**
- 📅 Google Calendar integration using **Service Account**
- 🗨️ Interactive **chat interface built with Streamlit**
- ⚡ FastAPI backend to handle event booking requests
- ✅ Fully hosted on **Render (free tier)**

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + Gemini (Google Generative AI API)
- **Backend**: FastAPI + Google Calendar API
- **LLM**: Gemini Pro (`google-generativeai`)
- **Hosting**: Render (frontend + backend)
- **Language**: Python 3.10+

---

## 🖼️ Architecture Overview

```text
User 🧑
  |
  v
Streamlit Chat Interface (Frontend)
  |
  v
Gemini Pro API (extracts intent)
  |
  v
FastAPI (Backend)
  |
  v
Google Calendar API (Event Created)
