import logging
from time import sleep
import os
from pydantic import BaseModel, Extra
from typing import List, Optional, Dict
from sws_api_client.generic_models import Code, Multilanguage
from sws_api_client.sws_api_client import SwsApiClient

logger = logging.getLogger(__name__)

class CodelistModel(BaseModel,  extra="allow"):
    id: str
    label: Multilanguage
    type: str

class Codelist(BaseModel, extra="allow"):
    model: CodelistModel
    codes: List[Code]

class Codelists:

    def __init__(self, sws_client: SwsApiClient) -> None:
        self.sws_client = sws_client

    def get_codelist(self, codelist_id: str, nocache = False) -> Codelist:

        url = f"/admin/reference/codelist/{codelist_id}?nocache={'true' if nocache else 'false'}"

        response = self.sws_client.discoverable.get('is_api', url)
        return Codelist(**response)