import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests
from loguru import logger

from sweepai.config.server import CACHE_DIRECTORY, POSTHOG_API_KEY
from sweepai.o11y.telemetry_utils import make_serializable_dict

POSTHOG_EVENTS_LOCATION = f"{CACHE_DIRECTORY}/posthog_events.txt"


def write_posthog_event_to_disk(event: str, properties: dict[str, Any] | None = None):
    try:
        properties["event"] = event
        full_payload = properties | {
            "event": event,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        stringified_payload = json.dumps(make_serializable_dict(full_payload)) + "\n"
    except Exception as e:
        logger.error(f"Error stringifying posthog event: {e}")
        return
    fd = os.open(POSTHOG_EVENTS_LOCATION, os.O_WRONLY | os.O_APPEND | os.O_CREAT)
    try:
        os.write(fd, stringified_payload.encode())
    except Exception as e:
        logger.error(f"Error writing posthog event to disk: {e}")
        os.close(fd)
        return
    finally:
        os.close(fd)


@dataclass
class PosthogClient:
    """
    Official Posthog API client has a thread leakage, so we are using a custom client.
    """

    API_KEY: str | None = None

    def capture(
        self,
        distinct_id: str | None = None,
        event: str | None = None,
        properties: dict[str, Any] | None = None,
        **kwargs,
    ):
        url = "https://app.posthog.com/capture/"
        headers = {"Content-Type": "application/json"}
        payload = {
            "api_key": self.API_KEY,
            "event": event,
            "properties": {"distinct_id": distinct_id, **properties},
            "timestamp": datetime.utcnow().isoformat() + "Z",  # Adding 'Z' to indicate UTC time
        }
        # always write to disk
        write_posthog_event_to_disk(event=event, properties=properties)
        if self.API_KEY is None:
            return  # don't fire off to posthog if we don't have an API key
        else:
            response = requests.post(url, headers=headers, data=json.dumps(make_serializable_dict(payload)))
            return response


posthog = PosthogClient(API_KEY=POSTHOG_API_KEY)
