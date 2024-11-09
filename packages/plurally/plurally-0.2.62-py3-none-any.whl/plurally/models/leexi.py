import base64
import os
import time
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import List

import requests
from loguru import logger
from pydantic import BaseModel, EmailStr, Field

from plurally.models.env_vars import BaseEnvVars
from plurally.models.node import Node

EXAMPLE_SUMMARY_OF_CALL = """
In the sales call, Alex from Plurally presented the benefits of Plurally’s CRM power-ups to John from SupaCompany, emphasizing how the tool could enhance SupaCompany's CRM capabilities with automation and AI-powered workflows. Alex highlighted the user-friendly, no-code interface, allowing teams to create and customize workflows easily, saving time and increasing efficiency. After discussing the specific needs of SupaCompany, John expressed interest in the solution. Alex then outlined the pricing, stating that the power-ups would be available for $9. They accepted to meet again next week to start using Plurally.
""".strip()


def get_basic_auth_header(username, password):
    return {
        "Authorization": "Basic "
        + base64.b64encode(f"{username}:{password}".encode()).decode()
    }


LEEXI_BASE_URL = "https://public-api.leexi.ai/v1"
LEEXI_DT_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"


class LeexiParticipant(BaseModel):
    name: str = Field(description="Name of the participant")
    email: EmailStr = Field(description="Email of the participant")


class Leexi(Node):
    IS_TRIGGER = True
    ICON = "leexi"

    class EnvVars(BaseEnvVars):
        LEEXI_API_KEY: str = Field(
            description="API key for the Leexi API",
            json_schema_extra={
                "help": "You can generate an API key/secret pair by going to [Leexi → Settings → Company Settings → API Keys](https://app.leexi.ai/settings/api_keys), and clicking on add (requires a Leexi admin account)."
            },
        )
        LEEXI_SECRET: str = Field(
            description="Secret for the Leexi API",
            json_schema_extra={
                "help": "[Leexi → Settings → Company Settings → API Keys](https://app.leexi.ai/settings/api_keys)."
            },
        )

    class InitSchema(Node.InitSchema):
        """
        This flow will be triggered as soon as a new recording is finished being processed by Leexi and there is a summary available. Leexi does not provide summaries for calls shorter than 90 seconds or calls longer than 3 hours.
        """

    class InputSchema(Node.InputSchema):
        pass

    class OutputSchema(Node.OutputSchema):
        summary: str = Field(
            description="Summary of the call",
            json_schema_extra={
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": "Summary of the call",
                },
                "example-default": EXAMPLE_SUMMARY_OF_CALL,
            },
        )
        participants: List[LeexiParticipant] = Field(
            description="Participants of the call",
            json_schema_extra={
                "name_singular": "Participant",
                "uiSchema": {"ui:label": False, "items": {"ui:label": False}},
                "example-default": [
                    {"name": "Alex", "email": "alex@tryplurally.com"},
                    {"name": "John", "email": "john@supacompany.com"},
                ],
            },
        )
        performed_at: datetime = Field(description="Time when the call was performed")

    def __init__(self, node_inputs: InitSchema):
        if os.environ.get("PLURALLY_START_ISO_TIMESTAMP"):
            self.check_after = datetime.fromisoformat(
                os.environ["PLURALLY_START_ISO_TIMESTAMP"]
            )
        else:
            self.check_after = datetime.now(timezone.utc).replace(tzinfo=None)
        super().__init__(node_inputs)

    def get_auth_header(self):
        api_key = os.environ.get("LEEXI_API_KEY")
        assert api_key, "LEEXI_API_KEY is required"

        secret = os.environ.get("LEEXI_SECRET")
        assert secret, "LEEXI_SECRET is required"
        return get_basic_auth_header(api_key, secret)

    @lru_cache(maxsize=10)
    def get_calls(self, ttl_hash: int):
        url = LEEXI_BASE_URL + "/calls"
        calls = requests.get(
            url,
            headers=self.get_auth_header(),
            params={
                "items": 100,
                "from": self.check_after.strftime(LEEXI_DT_FMT),
                "order": "created_at asc",
            },
        )
        try:
            calls.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                raise RuntimeError(
                    "Leexi API error: Unauthorized. Please check your API key and secret."
                )
        res = calls.json()
        if res.get("success") is False:
            raise RuntimeError(f"Leexi API error: {res.get('message')}")
        return res

    def forward(self, *args, **kwargs):
        self.outputs = None
        calls = self.get_calls(ttl_hash=time.time() // 60)  # 1 minute TTL FIXME
        calls = calls.get("data")
        if calls:
            for call in calls:
                if call.get("summary"):
                    logger.debug("Found call with summary")
                    self.check_after = datetime.strptime(
                        call["created_at"], LEEXI_DT_FMT
                    ) + timedelta(seconds=1)
                    self.outputs = self.OutputSchema(
                        summary=call["summary"],
                        participants=[
                            LeexiParticipant(name=p["name"], email=p["email"])
                            for p in call.get("participating_users", [])
                            if p.get("email") and p.get("name")
                        ],
                        performed_at=call["performed_at"],
                        # prompts=call.get("prompts"), maybe we could add this
                    ).model_dump()
                    return
                else:
                    logger.debug("No summary found in call")
