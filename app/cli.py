from datetime import datetime
from typing import Annotated

from rich import print
from typer import Argument, Option, Typer

from app.auth import authenticate, refresh_token
from app.google_calendar import create_event as create_calendar_event
from app.google_calendar import list_events as list_calendar_events

app = Typer()


@app.command()
def list(
    max_results: Annotated[
        int, Option(help="The maximum number of events to return.")
    ] = 10
):
    """List the next MAX_RESULTS events from the calendar."""
    print("Listing events...")
    events = list_calendar_events(max_results)
    if not events:
        print("No upcoming events found.")
        return
    for event in events:
        start_info = event["start"]
        end_info = event["end"]
        if "dateTime" in start_info:
            start_str = start_info["dateTime"]
            end_str = end_info["dateTime"]
            start_dt = datetime.fromisoformat(start_str)
            end_dt = datetime.fromisoformat(end_str)
            duration = end_dt - start_dt
            formatted_start = start_dt.strftime("%Y-%m-%d %H:%M")
            formatted_end = end_dt.strftime("%H:%M")
            print(
                f"{formatted_start} - {formatted_end} ({duration}) - {event['summary']}"
            )
        else:
            start_str = start_info["date"]
            print(f"{start_str} (all day) - {event['summary']}")


@app.command()
def create(
    summary: Annotated[
        str, Argument(help="The summary or title of the event.")
    ],
    start_time: Annotated[
        datetime, Argument(help="The start time of the event in ISO format.")
    ],
    end_time: Annotated[
        datetime, Argument(help="The end time of the event in ISO format.")
    ],
    description: Annotated[
        str | None, Option(help="A description of the event.")
    ] = None,
    location: Annotated[
        str | None, Option(help="The location of the event.")
    ] = None,
):
    """Create a new event in the calendar."""
    print("Creating event...")
    create_calendar_event(summary, start_time, end_time, description, location)


@app.command()
def auth():
    """Refresh the authentication token."""
    if refresh_token():
        print("Authentication token refreshed.")
    else:
        print("No authentication token found. Starting authentication flow...")
        authenticate()
        print("Authentication complete!")
