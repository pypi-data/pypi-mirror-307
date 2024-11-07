import logging
from typing import List, Dict, Optional, TypedDict, Union
from enum import Enum
from sws_api_client.sws_api_client import SwsApiClient

logger = logging.getLogger(__name__)

# Enum definitions
class TableLayer(str, Enum):
    GOLD = 'gold'
    SILVER = 'silver'
    BRONZE = 'bronze'
    STAGING = 'staging'
    CACHE = 'cache'

class TableType(str, Enum):
    SDMX_CSV = 'SDMX-csv'
    CSV = 'csv'
    ICEBERG = 'iceberg'

class DisseminationTarget(str, Enum):
    SDW = 'sdw'
    FAOSTAT = 'faostat'

class Platform(str, Enum):
    STAT = '.stat'
    MDM = 'mdm'

class DisseminationStepStatus(str, Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'

class DisseminationAction(str, Enum):
    INSERT = 'I'
    APPEND = 'A'
    REPLACE = 'R'
    DELETE = 'D'

# Type definitions
class LifecycleHistory(TypedDict):
    modifiedOn: str
    modifiedBy: str
    description: str

class Lifecycle(TypedDict):
    createdOn: str
    createdBy: str
    history: List[LifecycleHistory]

class Column(TypedDict):
    name: str
    type: str
    description: str

class Structure(TypedDict):
    columns: List[Column]

class BaseDisseminatedTagTable(TypedDict):
    id: str
    name: str
    description: str
    layer: TableLayer
    private: bool
    type: TableType
    database: Optional[str]
    table: Optional[str]
    path: Optional[str]
    structure: Structure

class DisseminatedTagTable(BaseDisseminatedTagTable):
    lifecycle: Lifecycle

class BaseDisseminatedTag(TypedDict):
    domain: str
    dataset: str
    name: str
    disseminatedTagid: str
    description: Optional[str]

class DisseminationStepInfo(TypedDict, total=False):
    endpoint: Optional[str]
    structure: Optional[str]
    structure_id: Optional[str]
    action: Optional[DisseminationAction]
    dataspace: Optional[str]

class BaseDisseminationStep(TypedDict):
    target: DisseminationTarget
    platform: Optional[Platform]
    startedOn: str
    endedOn: str
    status: DisseminationStepStatus
    table: str
    info: Optional[DisseminationStepInfo]

class DisseminationStep(BaseDisseminationStep):
    user: str

class DisseminatedTagInfo(TypedDict):
    disseminationSteps: List[DisseminationStep]
    tables: List[DisseminatedTagTable]

class DisseminatedTag(BaseDisseminatedTag):
    createdOn: str
    disseminationSteps: List[DisseminationStep]
    tables: List[DisseminatedTagTable]

class PaginatedResponseLight(TypedDict):
    items: List[BaseDisseminatedTag]
    next: Optional[str]

class PaginatedResponse(TypedDict):
    items: List[DisseminatedTag]
    next: Optional[str]

class Tags:

    def __init__(self, sws_client: SwsApiClient, endpoint: str = 'tag_api') -> None:
        self.sws_client = sws_client
        self.endpoint = endpoint

    def get_read_access_url(self, path: str, expiration: int) -> Dict:
        url = "/tags/dissemination/getReadAccessUrl"
        body = {"path": path, "expiration": expiration}
        response = self.sws_client.discoverable.post(self.endpoint, url, data=body)
        return response

    def get_all_disseminated_tags(self, limit: int, next_token: Optional[str] = None) -> PaginatedResponseLight:
        url = "/tags/dissemination/all"
        params = {"limit": limit, "next": next_token}
        response = self.sws_client.discoverable.get(self.endpoint, url, params=params)
        return response

    def get_disseminated_tags_by_dataset(self, dataset: str, limit: int, next_token: Optional[str] = None) -> PaginatedResponse:
        url = f"/tags/dissemination/dataset/{dataset}"
        params = {"limit": limit, "next": next_token}
        response = self.sws_client.discoverable.get(self.endpoint, url, params=params)
        return response

    def get_disseminated_tag(self, dataset: str, tag_id: str) -> Optional[DisseminatedTag]:
        url = f"/tags/dissemination/dataset/{dataset}/{tag_id}"
        response = self.sws_client.discoverable.get(self.endpoint, url)
        if not response:
            return None
        return response
    
    def create_disseminated_tag(self, dataset: str, name: str, tag_id: str, description: Optional[str] = None) -> DisseminatedTag:
        url = "/tags/dissemination"
        body = {
            "dataset": dataset,
            "name": name,
            "id": tag_id,
            "description": description
        }
        response = self.sws_client.discoverable.post(self.endpoint, url, data=body)
        return response

    def add_dissemination_table(self, dataset: str, tag_id: str, table: BaseDisseminatedTagTable) -> DisseminatedTag:
        url = f"/tags/dissemination/dataset/{dataset}/{tag_id}/table"
        body = {"table": table}
        
        response = self.sws_client.discoverable.post(self.endpoint, url, data=body)
        return response

    def update_dissemination_table(self, dataset: str, tag_id: str, table: DisseminatedTagTable) -> DisseminatedTag:
        url = f"/tags/dissemination/dataset/{dataset}/{tag_id}/table"
        body = {"table": table}
        print(body)
        print(url)
        response = self.sws_client.discoverable.put(self.endpoint, url, data=body)
        return response

    def add_dissemination_step(self, dataset: str, tag_id: str, step: BaseDisseminationStep) -> DisseminatedTag:
        url = f"/tags/dissemination/dataset/{dataset}/{tag_id}/step"
        body = {"step": step}
        response = self.sws_client.discoverable.post(self.endpoint, url, data=body)
        return response
