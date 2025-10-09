from datetime import datetime
from typing import Annotated

from rich.console import Console
from rich.table import Table
from typer import Argument, Option, Typer

from app.auth import authenticate, refresh_token
from app.google_calendar import (
    create_event as create_calendar_event,
)
from app.google_calendar import (
    delete_event as delete_calendar_event,
)
from app.google_calendar import (
    get_calendar_list as get_calendar_list_events,
)
from app.google_calendar import (
    get_event as get_calendar_event,
)
from app.google_calendar import (
    list_events as list_calendar_events,
)
from app.google_calendar import (
    search_events as search_calendar_events,
)
from app.google_calendar import (
    update_event as update_calendar_event,
)

app = Typer()
console = Console()


@app.command(name="list")
def list_events_command(
    max_results: Annotated[
        int, Option(help="The maximum number of events to return.")
    ] = 10,
    calendar_id: Annotated[
        str,
        Option(
            "--calendar-id",
            "-c",
            help="The ID of the calendar to list events from.",
        ),
    ] = "primary",
):
    """List the next MAX_RESULTS events from the calendar."""
    console.print(f"Listing events from calendar '{calendar_id}'...")
    events = list_calendar_events(max_results, calendar_id)
    if not events:
        console.print("No upcoming events found.")
        return

    table = Table(
        title="Upcoming Events", show_header=True, header_style="bold magenta"
    )
    table.add_column("Start", style="dim")
    table.add_column("End", style="dim")
    table.add_column("Duration")
    table.add_column("Summary")
    table.add_column("ID", style="dim")

    for event in events:
        start_info = event["start"]
        end_info = event["end"]
        if "dateTime" in start_info:
            start_dt = datetime.fromisoformat(start_info["dateTime"])
            end_dt = datetime.fromisoformat(end_info["dateTime"])
            duration = end_dt - start_dt
            table.add_row(
                start_dt.strftime("%A, %Y-%m-%d %H:%M"),
                end_dt.strftime("%H:%M"),
                str(duration),
                event["summary"],
                event["id"],
            )
        else:
            table.add_row(
                start_info["date"],
                "",
                "All day",
                event["summary"],
                event["id"],
            )
    console.print(table)


@app.command()
def calendars():
    """List all calendars the user has access to."""
    console.print("Getting calendar list...")
    calendars = get_calendar_list_events()
    if not calendars:
        console.print("No calendars found.")
        return

    table = Table(
        title="Available Calendars",
        show_header=True,
        header_style="bold magenta",
        expand=True,
    )
    table.add_column("Summary")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("Description", style="dim")

    for calendar in calendars:
        table.add_row(
            calendar.get("summary"),
            calendar.get("id"),
            calendar.get("description", "N/A"),
        )
    console.print(table)


@app.command()
def search(
    query: Annotated[str, Argument(help="The text to search for in event titles.")],
    max_results: Annotated[
        int, Option(help="The maximum number of events to return.")
    ] = 10,
    start_time: Annotated[
        datetime | None,
        Option(
            "--start-time",
            "-s",
            help="The start time for the search range.",
        ),
    ] = None,
    end_time: Annotated[
        datetime | None,
        Option(
            "--end-time",
            "-e",
            help="The end time for the search range.",
        ),
    ] = None,
    order: Annotated[
        str,
        Option(
            "--order",
            "-o",
            help="The order of the events. Can be 'startTime' or 'updated'.",
        ),
    ] = "startTime",
    calendar_id: Annotated[
        str,
        Option(
            "--calendar-id",
            "-c",
            help="The ID of the calendar to search in.",
        ),
    ] = "primary",
):
    """Search for events in the calendar."""
    console.print(
        f"Searching for events matching '{query}' in calendar '{calendar_id}'..."
    )
    events = search_calendar_events(
        query,
        max_results=max_results,
        start_time=start_time,
        end_time=end_time,
        order_by=order,
        calendar_id=calendar_id,
    )
    if not events:
        console.print("No events found.")
        return

    table = Table(
        title=f"Search Results for '{query}'",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Start", style="dim")
    table.add_column("End", style="dim")
    table.add_column("Duration")
    table.add_column("Summary")
    table.add_column("ID", style="dim")

    for event in events:
        start_info = event["start"]
        end_info = event["end"]
        if "dateTime" in start_info:
            start_dt = datetime.fromisoformat(start_info["dateTime"])
            end_dt = datetime.fromisoformat(end_info["dateTime"])
            duration = end_dt - start_dt
            table.add_row(
                start_dt.strftime("%A, %Y-%m-%d %H:%M"),
                end_dt.strftime("%H:%M"),
                str(duration),
                event["summary"],
                event["id"],
            )
        else:
            table.add_row(
                start_info["date"],
                "",
                "All day",
                event["summary"],
                event["id"],
            )
    console.print(table)


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
    attendees: Annotated[
        list[str] | None,
        Option(
            "--attendee",
            "-a",
            help="Email of an attendee to invite.",
        ),
    ] = None,
):
    """Create a new event in the calendar."""
    print("Creating event...")
    create_calendar_event(
        summary, start_time, end_time, description, location, attendees
    )


@app.command()
def delete(
    event_id: Annotated[str, Argument(help="The ID of the event to delete.")]
):
    """Delete an event from the calendar."""
    print(f"Deleting event {event_id}...")
    delete_calendar_event(event_id)


@app.command()
def get(
    event_id: Annotated[str, Argument(help="The ID of the event to get.")],
    calendar_id: Annotated[
        str,
        Option(
            "--calendar-id",
            "-c",
            help="The ID of the calendar to get the event from.",
        ),
    ] = "primary",
):
    """Get the details of a specific event."""
    console.print(
        f"Getting details for event {event_id} from calendar '{calendar_id}'..."
    )
    event = get_calendar_event(event_id, calendar_id)
    if not event:
        console.print("Event not found.")
        return

    table = Table(show_header=False, title="Event Details")
    table.add_column("Field", style="bold magenta")
    table.add_column("Value")

    table.add_row("Summary", event.get("summary", "N/A"))
    table.add_section()

    start_info = event["start"]
    end_info = event["end"]
    if "dateTime" in start_info:
        start_dt = datetime.fromisoformat(start_info["dateTime"])
        end_dt = datetime.fromisoformat(end_info["dateTime"])
        duration = end_dt - start_dt
        table.add_row("Start", start_dt.strftime("%A, %Y-%m-%d %H:%M"))
        table.add_row("End", end_dt.strftime("%H:%M"))
        table.add_row("Duration", str(duration))
    else:
        table.add_row("Start", start_info["date"])
        table.add_row("Duration", "All day")

    table.add_section()
    table.add_row("Description", event.get("description", "N/A"))
    table.add_row("Location", event.get("location", "N/A"))
    table.add_section()

    attendees = event.get("attendees")
    if attendees:
        attendee_list = "\n".join(
            [f"- {attendee.get('email')}" for attendee in attendees]
        )
        table.add_row("Attendees", attendee_list)
    else:
        table.add_row("Attendees", "N/A")

    console.print(table)


@app.command()
def update(
    event_id: Annotated[str, Argument(help="The ID of the event to update.")],
    summary: Annotated[
        str | None, Option(help="The new summary or title of the event.")
    ] = None,
    start_time: Annotated[
        datetime | None,
        Option(help="The new start time of the event in ISO format."),
    ] = None,
    end_time: Annotated[
        datetime | None,
        Option(help="The new end time of the event in ISO format."),
    ] = None,
    description: Annotated[
        str | None, Option(help="The new description of the event.")
    ] = None,
    location: Annotated[
        str | None, Option(help="The new location of the event.")
    ] = None,
    attendees: Annotated[
        list[str] | None,
        Option(
            "--attendee",
            "-a",
            help="New email of an attendee to invite.",
        ),
    ] = None,
):
    """Update an event in the calendar."""
    print(f"Updating event {event_id}...")
    update_calendar_event(
        event_id,
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        description=description,
        location=location,
        attendees=attendees,
    )


@app.command()
def auth():
    """Refresh the authentication token."""
    if refresh_token():
        print("Authentication token refreshed.")
    else:
        print("No authentication token found. Starting authentication flow...")
        authenticate()
        print("Authentication complete!")
