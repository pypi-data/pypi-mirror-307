"""This file contains functions to read and display posthog events from disk as html."""

import json

from sweepai.o11y.event_logger import POSTHOG_EVENTS_LOCATION


def read_posthog_events_from_disk() -> list[str]:
    """Reads posthog events from disk."""
    with open(POSTHOG_EVENTS_LOCATION, "r") as f:
        return f.readlines()


def format_posthog_events_as_csv(events: list[str]) -> str:
    """Format posthog events as a csv"""
    csv = "username,timestamp,event\n"
    for event in events:
        event_dict = json.loads(event)
        username = event_dict.get("username", "Unknown User")
        event_name = event_dict.get("event", "Unknown Event")
        timestamp = event_dict.get("timestamp", "Unknown Timestamp")
        csv += f"{username},{timestamp},{event_name}\n"
    return csv


if __name__ == "__main__":
    events = read_posthog_events_from_disk()
    csv = format_posthog_events_as_csv(events)
    with open("posthog_events.csv", "w") as f:
        f.write(csv)
