import datetime
from typing import Sequence

from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

from app.auth import authenticate


def list_events(max_results: int = 10) -> Sequence:
    """
    Lists the next max_results events on the user's calendar.
    """
    creds = authenticate()
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        print(f"Getting the upcoming {max_results} events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def create_event(
    summary: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    description: str | None = None,
    location: str | None = None,
):
    """Creates an event on the user's calendar."""
    creds = authenticate()
    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC",
            },
        }
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    events = list_events()
    if not events:
        print("No upcoming events found.")
    # Prints the start and name of the next 10 events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
