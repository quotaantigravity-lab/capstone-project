# app/agent.py

from __future__ import annotations

import re
import os
from typing import Any

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

# Load Gemini model securely using environment variables
model = Gemini(
    model="gemini-2.5-flash",
)

# Mock databases for user calendar
CALENDAR_EVENTS: list[dict[str, str]] = [
    {"time": "09:00", "title": "Morning Sync Session"},
    {"time": "12:00", "title": "Lunch with team"},
    {"time": "15:00", "title": "Focus Block"},
]

def sanitize_content(text: str) -> str:
    """Sanitizes sensitive information (PII) like phone numbers and physical addresses in a text.

    Args:
        text: The raw text content to sanitize.

    Returns:
        The sanitized text with sensitive PII replaced by '[REDACTED]'.
    """
    # Redact phone numbers (e.g., 0912345678, +1-555-0199, etc.)
    phone_pattern = r'(\b0\d{9}\b|\b\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b)'
    # Redact addresses (e.g., "123 Main St", "456 Oak Avenue")
    address_pattern = r'(?i)\b\d+\s+([a-z0-9\s]+)\s+(street|st|avenue|ave|road|rd|boulevard|blvd|lane|ln)\b'
    
    sanitized = re.sub(phone_pattern, '[REDACTED]', text)
    sanitized = re.sub(address_pattern, '[REDACTED]', sanitized)
    return sanitized

def list_calendar() -> str:
    """Retrieves list of all calendar events for the user.

    Returns:
        A text summary of calendar events.
    """
    events_str = "\n".join([f"- {e['time']}: {e['title']}" for e in CALENDAR_EVENTS])
    return f"Current calendar events:\n{events_str}"

def add_event(time: str, title: str) -> str:
    """Adds a new event to the user's calendar.

    Args:
        time: The time of the event (HH:MM).
        title: The title/description of the event.

    Returns:
        A confirmation message.
    """
    CALENDAR_EVENTS.append({"time": time, "title": title})
    return f"Successfully added event '{title}' at {time} to calendar."

def send_email_concierge(recipient: str, subject: str, body: str) -> str:
    """Sends a sanitized email message to a recipient.

    Args:
        recipient: The email address of the recipient.
        subject: The email subject.
        body: The body content of the email (will be sanitized for PII).

    Returns:
        A status message with the sanitized email body content.
    """
    sanitized_body = sanitize_content(body)
    return f"Email sent successfully to {recipient} with subject '{subject}'. Body: {sanitized_body}"

# Collaborative multi-agent setup
life_planner_agent = Agent(
    name="life_planner_agent",
    model=model,
    instruction=(
        "You are a personal concierge life planner. Help users organize their day, plan events, "
        "and draft emails. Coordinate with the secure_workspace_agent when the user wants to list "
        "their calendar, add events, or send emails."
    ),
    tools=[list_calendar, add_event],
)

secure_workspace_agent = Agent(
    name="secure_workspace_agent",
    model=model,
    instruction=(
        "You are a secure workspace integrator. Your role is to send emails and save logs. "
        "You MUST ensure that all emails are sent via the send_email_concierge tool to guarantee "
        "PII redaction before dispatch."
    ),
    tools=[send_email_concierge],
)

app = App(
    name="app",
    root_agent=life_planner_agent,
)
