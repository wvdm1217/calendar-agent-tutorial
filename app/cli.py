from datetime import datetime

from rich import print
from typer import Typer

from app.google_calendar import list_events as list_calendar_events

app = Typer()


@app.command()
def hello(name: str):
    """Say hello to NAME."""
    print(f"Hello {name}!")


@app.command()
def list_events(max_results: int = 10):
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
