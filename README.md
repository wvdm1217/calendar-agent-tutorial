# Calendar Agent Tutorial

The repo is a step by step guide for building a Google Calendar agent of increasing complexity.

## Requirements

- Python 3.13+
- Access to a Google Cloud Project (for Google Calendar API)
- Google Calendar API credentials (`credentials.json`)

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Obtain Google Calendar API credentials:**
   - Follow the instructions in the [Google Calendar API documentation](https://developers.google.com/calendar/api/quickstart/python)
   - Download your `credentials.json` file and place it in the project root
   - Change the redirect URL to 
   ```
   "redirect_uris": [
        "http://localhost:8888"
    ]
    ```

3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **First-time authentication:**
   ```bash
   calendar-agent list-events
   ```
   This will prompt you to authenticate with Google and create a `token.json` file.

## CLI Usage

The CLI provides commands to interact with your Google Calendar without using an LLM.

### List Events

List upcoming events from your calendar:

```bash
calendar-agent list-events [OPTIONS]
```

**Options:**
- `--max-results INTEGER`: The maximum number of events to return (default: 10)

**Example:**
```bash
calendar-agent list-events --max-results 20
```

**Output:**
```
2025-10-08 09:00 - 09:30 (0:30:00) - GenAI Standup
2025-10-08 09:30 - 10:00 (0:30:00) - Code Review
2025-10-08 (all day) - Office
```

### Create Event

Create a new event in your calendar:

```bash
calendar-agent create-event SUMMARY START_TIME END_TIME [OPTIONS]
```

**Arguments:**
- `SUMMARY`: The title of the event (required)
- `START_TIME`: The start time in ISO format (required)
- `END_TIME`: The end time in ISO format (required)

**Options:**
- `--description TEXT`: A description of the event
- `--location TEXT`: The location of the event

**Example:**
```bash
calendar-agent create-event "Team Meeting" "2025-10-09T14:00:00" "2025-10-09T15:00:00" \
  --description "Discuss Q4 planning" \
  --location "Conference Room A"
```

### Refresh Authentication

Manually refresh your authentication token:

```bash
calendar-agent refresh-auth
```

This command is useful when you need to update your access token without waiting for it to expire.

## Agent Iterations

1. **CLI:** ✅ A CLI that does not use a LLM. 
2. **Simple Agent:** An agent that converts a user prompt to a meeting invite.
3. **Tool Use Agent:** An agent that has context of the current time when creating meetings. 
4. **Reasoning Agent:** The agent is able to resolve conflicts in my existing calendar.

## Project Structure

```
calendar-agent-tutorial/
├── app/
│   ├── auth.py              # Authentication logic
│   ├── cli.py               # CLI commands
│   ├── config.py            # Configuration settings
│   └── google_calendar.py   # Google Calendar API interactions
├── credentials.json         # Google API credentials (not in repo)
├── token.json              # OAuth token (auto-generated)
├── pyproject.toml          # Project dependencies
└── README.md
```