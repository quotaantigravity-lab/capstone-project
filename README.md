# SecureLifePlanner: A PII-Safe Personal Concierge & Workspace Organizer

**SecureLifePlanner** is a secure, personal concierge AI assistant built using the Google **Agent Development Kit (ADK) 2.0** for the Kaggle Capstone Project under the **Concierge Agents** track. 

It organizes everyday tasks and coordinates calendars while enforcing strict data filtering boundaries to protect sensitive personal identifiable information (PII) before any outbound email or log leaves the system.

---

## 🚀 Key Features

*   **Daily Agenda Organizer:** Reads, structures, and updates the user's daily calendar events.
*   **Smart Workspace Coordination:** Books slots and drafts email updates to coordinate tasks with others.
*   **Automated PII Masking:** Scans inputs and dynamically redacts phone numbers, street addresses, and sensitive identification numbers into `[REDACTED]` prior to external transmission.
*   **Static Scanning Gating:** Custom git pre-commit hooks that actively scan the codebase to prevent credential leakage.
*   **PreToolUse Interception:** Antigravity hooks that intercept command-line invocations to block destructive actions.

---

## 📐 Multi-Agent Architecture (ADK 2.0)

SecureLifePlanner splits reasoning and execution using a collaborative agent graph:
*   **`life_planner_agent`**: Actively chats with the user, maps their requirements, lists events, and schedules new slots using calendar tools.
*   **`secure_workspace_agent`**: Interacts with email and file tools. All outbound emails must be dispatched via the `send_email_concierge` tool, which enforces the `pii-leak-prevention` skill to sanitize content before sending.

```
                  ┌────────────────────────┐
                  │          USER          │
                  └───────────┬────────────┘
                              │ Prompt
                              ▼
                  ┌────────────────────────┐
                  │   life_planner_agent   │◄───► [Calendar Tools]
                  └───────────┬────────────┘
                              │ Delegated Task
                              ▼
                  ┌────────────────────────┐
                  │ secure_workspace_agent │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │  pii-leak-prevention   │ (Skill)
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │  send_email_concierge  │ (PII Masked & Sent)
                  └────────────────────────┘
```

---

## 🔒 Security Boundaries & Guardrails

This project shifts security left to the local development environment:

1.  **PII Leak Prevention Skill:** Detailed in `.agents/skills/pii-leak-prevention/SKILL.md`, it guides the LLM to identify and redact sensitive data.
2.  **Antigravity Command Hook:** Configured in `.agents/hooks.json` to trigger `.agents/scripts/validate_tool_call.py` to prevent execution of destructive shell actions.
3.  **Git Pre-commit Semgrep SCAN:** Configured in `.pre-commit-config.yaml` to run `semgrep_windows.py` which blocks any git commits containing hardcoded Google API credentials.

---

## 🧪 Automated Tests

The security boundaries are validated with a Pytest suite:
```bash
uv run pytest tests/test_agent.py
```
This tests:
*   Redaction of diverse phone number formats.
*   Redaction of physical street addresses.
*   Automatic email payload sanitization before dispatch.

---

## 🛠️ How to Run

### Prerequisites
*   [uv](https://docs.astral.sh/uv/) (Fast Python package manager)
*   [google-agents-cli](https://pypi.org/project/google-agents-cli/)

### Setup
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    agents-cli install
    ```
3.  Configure environment variables with your Gemini API key:
    ```bash
    export GEMINI_API_KEY="your-api-key-here"
    export GOOGLE_GENAI_USE_VERTEXAI="False"
    ```
4.  Launch the playground to interact with the agent:
    ```bash
    agents-cli playground
    ```
    Access the UI at: `http://127.0.0.1:8080/dev-ui/?app=app`
