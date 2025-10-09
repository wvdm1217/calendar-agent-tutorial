import datetime
from typing import Annotated

from app.google_calendar import (
    create_event,
    delete_event,
    get_calendar_list,
    get_event,
    list_events,
    search_events,
    update_event,
)


def get_tools():
    return [
        get_current_time,
        list_calendar_events,
        search_calendar_events,
        get_calendar_event,
        create_calendar_event,
        update_calendar_event,
        delete_calendar_event,
        get_calendars,
    ]


def get_current_time() -> str:
    """
    Gets the current date and time.
    Use this when the user asks about relative dates like 'tomorrow', 'next week', 'today', etc.
    This helps you calculate the correct dates for calendar operations.
    Returns the current date and time in ISO format with timezone information.
    """
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    return f"Current date and time: {now.isoformat()} (UTC)"


def list_calendar_events(
    max_results: Annotated[int, "The maximum number of events to return"] = 10,
    calendar_id: Annotated[str, "The ID of the calendar to list events from"] = "primary",
) -> str:
    """
    Lists the next upcoming events on the user's calendar.
    Use this when the user asks to see their upcoming events, schedule, or what's on their calendar.
    Returns a list of events with their start times, end times, and summaries.
    """
    events = list_events(max_results, calendar_id)
    if not events:
        return "No upcoming events found."
    
    result = ["Upcoming events:\n"]
    for event in events:
        start_info = event["start"]
        end_info = event["end"]
        if "dateTime" in start_info:
            start_dt = datetime.datetime.fromisoformat(start_info["dateTime"])
            end_dt = datetime.datetime.fromisoformat(end_info["dateTime"])
            result.append(
                f"• {event['summary']}\n"
                f"  Date: {start_dt.strftime('%A, %Y-%m-%d')}\n"
                f"  Time: {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}\n"
                f"  ID: {event['id']}\n"
            )
        else:
            result.append(
                f"• {event['summary']}\n"
                f"  Date: {start_info['date']} (All-day)\n"
                f"  ID: {event['id']}\n"
            )
    
    return "\n".join(result)


def search_calendar_events(
    query: Annotated[str, "The text to search for in event titles and descriptions"],
    max_results: Annotated[int, "The maximum number of events to return"] = 10,
    calendar_id: Annotated[str, "The ID of the calendar to search in"] = "primary",
) -> str:
    """
    Searches for events on the user's calendar by keyword.
    Use this when the user asks to find specific events or meetings.
    Returns a list of matching events.
    """
    events = search_events(query, max_results=max_results, calendar_id=calendar_id)
    if not events:
        return f"No events found matching '{query}'."
    
    result = [f"Events matching '{query}':\n"]
    for event in events:
        start_info = event["start"]
        if "dateTime" in start_info:
            start_dt = datetime.datetime.fromisoformat(start_info["dateTime"])
            result.append(
                f"• {event['summary']}\n"
                f"  Date: {start_dt.strftime('%A, %Y-%m-%d')}\n"
                f"  Time: {start_dt.strftime('%H:%M')}\n"
                f"  ID: {event['id']}\n"
            )
        else:
            result.append(
                f"• {event['summary']}\n"
                f"  Date: {start_info['date']} (All-day)\n"
                f"  ID: {event['id']}\n"
            )
    
    return "\n".join(result)


def get_calendar_event(
    event_id: Annotated[str, "The ID of the event to retrieve"],
    calendar_id: Annotated[str, "The ID of the calendar"] = "primary",
) -> str:
    """
    Gets the details of a specific calendar event.
    Use this when the user asks for more information about a particular event.
    Requires the event ID which can be obtained from list_calendar_events or search_calendar_events.
    """
    event = get_event(event_id, calendar_id)
    if not event:
        return f"Event with ID {event_id} not found."
    
    start_info = event["start"]
    end_info = event["end"]
    details = [f"Summary: {event.get('summary', 'N/A')}"]
    
    if "dateTime" in start_info:
        details.append(f"Start: {start_info['dateTime']}")
        details.append(f"End: {end_info['dateTime']}")
    else:
        details.append(f"Date: {start_info['date']} (All-day)")
    
    if event.get("description"):
        details.append(f"Description: {event['description']}")
    if event.get("location"):
        details.append(f"Location: {event['location']}")
    if event.get("attendees"):
        attendees = ", ".join([a.get("email", "") for a in event["attendees"]])
        details.append(f"Attendees: {attendees}")
    
    return "\n".join(details)


def create_calendar_event(
    summary: Annotated[str, "The title/summary of the event"],
    start_time: Annotated[str, "Start time in ISO format (e.g., 2025-10-09T14:00:00)"],
    end_time: Annotated[str, "End time in ISO format (e.g., 2025-10-09T15:00:00)"],
    description: Annotated[str | None, "Optional description of the event"] = None,
    location: Annotated[str | None, "Optional location of the event"] = None,
    attendees: Annotated[list[str] | None, "Optional list of attendee email addresses"] = None,
) -> str:
    """
    Creates a new event on the user's calendar.
    Use this when the user asks to schedule, create, or add a new event or meeting.
    Times should be in ISO format.
    """
    try:
        start_dt = datetime.datetime.fromisoformat(start_time)
        end_dt = datetime.datetime.fromisoformat(end_time)
        create_event(summary, start_dt, end_dt, description, location, attendees)
        return f"Successfully created event '{summary}' from {start_time} to {end_time}."
    except Exception as e:
        return f"Error creating event: {str(e)}"


def update_calendar_event(
    event_id: Annotated[str, "The ID of the event to update"],
    summary: Annotated[str | None, "New title/summary of the event"] = None,
    start_time: Annotated[str | None, "New start time in ISO format"] = None,
    end_time: Annotated[str | None, "New end time in ISO format"] = None,
    description: Annotated[str | None, "New description of the event"] = None,
    location: Annotated[str | None, "New location of the event"] = None,
) -> str:
    """
    Updates an existing event on the user's calendar.
    Use this when the user asks to modify, change, or update an event.
    Only provide the fields that need to be updated.
    """
    try:
        kwargs = {}
        if summary:
            kwargs["summary"] = summary
        if start_time:
            kwargs["start_time"] = datetime.datetime.fromisoformat(start_time)
        if end_time:
            kwargs["end_time"] = datetime.datetime.fromisoformat(end_time)
        if description:
            kwargs["description"] = description
        if location:
            kwargs["location"] = location
        
        update_event(event_id, **kwargs)
        return f"Successfully updated event {event_id}."
    except Exception as e:
        return f"Error updating event: {str(e)}"


def delete_calendar_event(
    event_id: Annotated[str, "The ID of the event to delete"],
) -> str:
    """
    Deletes an event from the user's calendar.
    Use this when the user asks to cancel, remove, or delete an event.
    This action cannot be undone.
    """
    try:
        delete_event(event_id)
        return f"Successfully deleted event {event_id}."
    except Exception as e:
        return f"Error deleting event: {str(e)}"


def get_calendars() -> str:
    """
    Gets the list of all calendars the user has access to.
    Use this when the user asks what calendars they have or wants to see all their calendars.
    """
    calendars = get_calendar_list()
    if not calendars:
        return "No calendars found."
    
    result = []
    for calendar in calendars:
        result.append(f"- {calendar.get('summary')} (ID: {calendar.get('id')})")
    
    return "\n".join(result)