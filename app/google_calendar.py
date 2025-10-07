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


if __name__ == "__main__":
    events = list_events()
    if not events:
        print("No upcoming events found.")
    # Prints the start and name of the next 10 events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
