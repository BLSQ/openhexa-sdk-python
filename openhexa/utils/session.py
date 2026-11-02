"""Custom HttpClient with retry mechanism."""


import functools
import importlib.util
import os
import urllib.request
from importlib.metadata import version

import requests
import requests.utils
import urllib3
import urllib3.connection
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


def install_default_user_agent():
    """Make `get_user_agent()` the default User-Agent of requests, urllib, urllib3 and httpx.

    Meant to be called once at interpreter startup (from the base image's sitecustomize), so that requests made by
    pipeline code with any of these libraries identify the pipeline. A User-Agent set explicitly by the caller still
    wins. Set HEXA_DISABLE_USER_AGENT_PATCH to a true value to disable it.
    """
    if os.environ.get("HEXA_DISABLE_USER_AGENT_PATCH", "").strip().lower() in ("1", "true", "yes", "on"):
        return

    user_agent = get_user_agent()

    # Session() builds its default headers through requests.utils.default_headers(), which calls this at runtime.
    requests.utils.default_user_agent = lambda name="python-requests": user_agent

    # Covers urlopen(), build_opener() and libraries built on them (e.g. pandas.read_csv(url)). Unwrap a previous
    # patch so that calling this twice does not stack wrappers.
    init = urllib.request.OpenerDirector.__init__
    original_init = init.__wrapped__ if getattr(init, "_openhexa_patched", False) else init

    @functools.wraps(original_init)
    def opener_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.addheaders = [("User-agent", user_agent)]

    opener_init._openhexa_patched = True
    urllib.request.OpenerDirector.__init__ = opener_init

    # Private API, checked against urllib3 2.x: HTTPConnection.request() calls it when no User-Agent is given.
    urllib3.connection._get_default_user_agent = lambda: user_agent

    # Private API, checked against httpx 0.28: read by Client() when building its default headers. Only a missing
    # httpx is tolerated: if httpx._client moves in a future version, the import error must reach the caller.
    if importlib.util.find_spec("httpx") is not None:
        import httpx._client

        httpx._client.USER_AGENT = user_agent


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
