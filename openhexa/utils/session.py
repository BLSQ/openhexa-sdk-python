"""Custom HttpClient with retry mechanism."""


import requests
import urllib3
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def create_requests_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    verify=True,
) -> Session:
    """Return a Session object with retry capability."""
    session = requests.Session()
    session.verify = verify

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
