---
name: pii-leak-prevention
description: Guides the agent to identify, mask, and redact personally identifiable information (PII) before any outbound transmission.
---

# PII Leak Prevention Skill

## Goal
Enforce strict privacy filters to protect user sensitive data in personal assistant scenarios.

## Instructions
1. **Identify PII**: Systematically inspect all inputs, drafts, and messages for sensitive information:
   - Phone numbers (e.g., matching regional or international structures like 0912345678 or +1-555-0199).
   - Physical addresses containing street numbers, street names, and suffixes (e.g., 123 Main St).
   - Personal identification numbers (e.g., Passport or SSN).
2. **Redact Prior to Tool Invocation**: Before calling `send_email_concierge` or writing logs, pass the content through the sanitization logic. Replace matches with `[REDACTED]`.
3. **Verify Compliance**: Ensure no raw PII appears in any email body parameters.
