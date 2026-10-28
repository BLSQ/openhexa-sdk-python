"""Custom HttpClient with retry mechanism."""


import os
from importlib.metadata import version

import requests
import urllib3
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def get_user_agent() -> str:
    """Return the User-Agent of the SDK, identifying the current pipeline when running in a pipeline context.

    This allows third-party services to track traffic coming from a given pipeline, e.g.
    "openhexa-sdk/2.22.7 (workspace=my-workspace; pipeline=my-pipeline; run_id=<uuid>)".
    """
    user_agent = f"openhexa-sdk/{version('openhexa.sdk')}"
    context = {
        "workspace": os.environ.get("HEXA_WORKSPACE"),
        "pipeline": os.environ.get("HEXA_PIPELINE_CODE"),
        "run_id": os.environ.get("HEXA_RUN_ID"),
    }
    comment = "; ".join(f"{key}={value}" for key, value in context.items() if value)
    return f"{user_agent} ({comment})" if comment else user_agent


def create_requests_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    verify=True,
) -> Session:
    """Return a Session object with retry capability."""
    session = requests.Session()
    session.verify = verify
    session.headers["User-Agent"] = get_user_agent()

    if not verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
