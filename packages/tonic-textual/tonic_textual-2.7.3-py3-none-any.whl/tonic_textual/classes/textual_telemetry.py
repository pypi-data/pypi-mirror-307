import logging
import traceback
import os

from amplitude import Amplitude, BaseEvent
from typing import Optional

import requests

from tonic_textual.classes.httpclient import HttpClient

AMPLITUDE_API_KEY = os.getenv(
    "TONIC_TEXTUAL_ANALYTICS_KEY", "d04b22d8940cf7a21c5c86a803f3c709"
)


class TextualTelemetry:
    def __init__(
        self, base_url: str, api_key: Optional[str] = None, verify: bool = True
    ):
        try:
            if api_key is None:
                api_key = os.environ.get("TONIC_TEXTUAL_API_KEY")
                if api_key is None:
                    raise Exception(
                        "No API key provided. Either provide an API key, or set the API "
                        "key as the value of the TEXTUAL_API_KEY environment "
                        "variable."
                    )
            self.api_key = api_key
            self.client = HttpClient(base_url, self.api_key, verify)
            self.verify = verify

            with requests.Session() as session:
                response = self.client.http_get("/api/accounts", session=session)
                self.user_id = response.get("userName", "sdk_unknown_user")

            self.telemetry_client = Amplitude(AMPLITUDE_API_KEY)
            self.telemetry_client.configuration.flush_max_retries = 5
            self.telemetry_client.configuration.logger = logging.getLogger(__name__)
            self.telemetry_client.configuration.server_zone = "US"

            self.enabled = os.getenv("TONIC_TEXTUAL_SDK_TELEMETRY", "True").lower() in (
                "true",
                "1",
                "t",
            )
            self.telemetry_client.configuration.opt_out = not self.enabled
        except Exception as _:
            self.enabled = False

    def log_function_call(self):
        try:
            if not self.enabled:
                return

            # get the function call from the stack
            stack = traceback.extract_stack()

            called_function, parent_caller = stack[-2], stack[-3]

            if "tonic_textual" in parent_caller.filename:
                return
            else:
                # send amplitude event if function was directly called by user code
                event = BaseEvent(
                    event_type="SDK Call",
                    event_properties={"function_name": called_function.name},
                    user_id=self.user_id,
                )
                self.telemetry_client.track(event)
        except Exception as _:
            return
