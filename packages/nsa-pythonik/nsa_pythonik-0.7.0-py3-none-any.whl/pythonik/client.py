import json
from pydantic import BaseModel
from urllib3.util import Retry
from typing import Type, Optional, Union, List
from urllib.parse import urljoin
from requests import Session, Request, Response, PreparedRequest
from requests.adapters import HTTPAdapter

from pythonik.specs.assets import AssetSpec
from pythonik.specs.files import FilesSpec
from pythonik.specs.jobs import JobSpec
from pythonik.specs.metadata import MetadataSpec
from pythonik.specs.search import SearchSpec


# Iconik APIs
class PythonikClient:
    """
    Iconik Client
    """

    def __init__(self, app_id: str, auth_token: str, timeout: int):
        self.session = Session()
        retry_strategy = Retry(
            total=4,  # Maximum number of retries
            backoff_factor=3,
        )
        http_adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", http_adapter)
        self.session.mount("https://", http_adapter)
        self.session.headers = {
            "App-ID": app_id,
            "Auth-Token": auth_token,
            "Accept": "application/json",
        }
        self.timeout = timeout

    def assets(self):
        return AssetSpec(self.session, self.timeout)

    def files(self):
        return FilesSpec(self.session, self.timeout)

    def metadata(self):
        return MetadataSpec(self.session, self.timeout)

    def search(self):
        return SearchSpec(self.session, self.timeout)

    def jobs(self):
        return JobSpec(self.session, self.timeout)
