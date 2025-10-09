import datetime
from typing import Sequence

from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

from app.auth import authenticate


def list_events(max_results: int = 10, calendar_id: str = "primary") -> Sequence:
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
                calendarId=calendar_id,
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
    attendees: list[str] | None = None,
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
            "attendees": [{"email": email} for email in attendees] if attendees else [],
        }
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_event(event_id: str, calendar_id: str = "primary"):
    """Gets a specific event from the user's calendar."""
    creds = authenticate()
    try:
        service = build("calendar", "v3", credentials=creds)
        event = (
            service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        )
        return event

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def update_event(event_id: str, **kwargs):
    """Updates an event on the user's calendar."""
    creds = authenticate()
    try:
        service = build("calendar", "v3", credentials=creds)
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        for key, value in kwargs.items():
            if value is not None:
                if key in ["start_time", "end_time"]:
                    event[key.replace("_time", "")] = {
                        "dateTime": value.isoformat(),
                        "timeZone": "UTC",
                    }
                elif key == "attendees":
                    event["attendees"] = [{"email": email} for email in value]
                else:
                    event[key] = value

        updated_event = (
            service.events()
            .update(calendarId="primary", eventId=event_id, body=event)
            .execute()
        )
        print(f"Event updated: {updated_event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


def delete_event(event_id: str):
    """Deletes an event from the user's calendar."""
    creds = authenticate()
    try:
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print("Event deleted.")

    except HttpError as error:
        print(f"An error occurred: {error}")


def search_events(
    query: str,
    max_results: int = 10,
    start_time: datetime.datetime | None = None,
    end_time: datetime.datetime | None = None,
    order_by: str = "startTime",
    calendar_id: str = "primary",
) -> Sequence:
    """Searches for events on the user's calendar."""
    creds = authenticate()
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start_time = start_time or now

        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                q=query,
                timeMin=start_time.isoformat(),
                timeMax=end_time.isoformat() if end_time else None,
                maxResults=max_results,
                singleEvents=True,
                orderBy=order_by,
            )
            .execute()
        )
        return events_result.get("items", [])

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def get_calendar_list() -> Sequence:
    """Gets the user's calendar list."""
    creds = authenticate()
    try:
        service = build("calendar", "v3", credentials=creds)
        calendar_list = service.calendarList().list().execute()
        return calendar_list.get("items", [])

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


if __name__ == "__main__":
    events = list_events()
    if not events:
        print("No upcoming events found.")
    # Prints the start and name of the next 10 events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
