# capstone-project/tests/test_agent.py
import pytest
from app.agent import sanitize_content, send_email_concierge

def test_sanitize_content_redacts_phone_numbers():
    """Verify that typical phone number patterns are redacted."""
    raw_text = "Call me at 0912345678 or my office line +1-555-123-4567."
    sanitized = sanitize_content(raw_text)
    
    assert "0912345678" not in sanitized
    assert "+1-555-123-4567" not in sanitized
    assert sanitized.count("[REDACTED]") == 2

def test_sanitize_content_redacts_addresses():
    """Verify that physical street address patterns are redacted."""
    raw_text = "Deliver the package to 123 Main St or 456 Oak Avenue."
    sanitized = sanitize_content(raw_text)
    
    assert "123 Main St" not in sanitized
    assert "456 Oak Avenue" not in sanitized
    assert "[REDACTED]" in sanitized

def test_send_email_redacts_body_automatically():
    """Verify that the email sender tool automatically redacts PII before dispatch."""
    body_content = "Here is my info: John Doe, phone 0912345678, living at 12 Elm Road."
    res = send_email_concierge("manager@company.com", "My Info Update", body_content)
    
    assert "0912345678" not in res
    assert "12 Elm Road" not in res
    # Ensure recipient and subject are unchanged
    assert "manager@company.com" in res
    assert "My Info Update" in res
    # Ensure redactions took place
    assert "[REDACTED]" in res

def test_no_leakage_for_safe_texts():
    """Verify that safe daily tasks do not trigger false redactions."""
    safe_text = "Meeting at 10:00 AM with product team. Discuss project roadmap."
    sanitized = sanitize_content(safe_text)
    
    assert sanitized == safe_text
    assert "[REDACTED]" not in sanitized
