import logging
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from sws_api_client.sws_api_client import SwsApiClient
logger = logging.getLogger(__name__)
from datetime import datetime, time
from time import sleep

class LabelModel(BaseModel):
    en: str

class DescriptionModel(BaseModel):
    en: str

class ColumnModel(BaseModel):
    id: str
    label: LabelModel
    description: DescriptionModel
    type: str
    constraints: List[Any]
    defaultValue: Optional[Any]
    facets: List[Any]

class DataModel(BaseModel):
    url: Optional[str]
    available: bool
    uptodate: bool

class DatatableModel(BaseModel):
    id: str
    name: str
    label: LabelModel
    description: DescriptionModel
    schema_name: str = Field(..., alias="schema")
    domains: List[str]
    plugins: List[Any]
    columns: List[ColumnModel]
    facets: List[Any]
    last_update: datetime
    data: DataModel

class Datatables:

    def __init__(self, sws_client: SwsApiClient) -> None:
        self.sws_client = sws_client
    
    def get_datatable_info(self, datatable_id: str) -> DatatableModel:

        url = f"/datatables/{datatable_id}"

        response = self.sws_client.discoverable.get('datatable_api', url)
        if(response.get('id') is not None):
            return DatatableModel(**response)
        else:
            return None
        
    
    def invoke_export_datatable(self, datatable_id: str) -> Dict:

        url = f"/datatables/{datatable_id}/invoke_export_2_s3"

        response = self.sws_client.discoverable.post('datatable_api', url)

        return response

    def get_datatable_csv_path(self, datatable, timeout=60*15, interval=2) -> HttpUrl:

        info = self.get_datatable_info(datatable)
        if info.data.available:
            return info.data.url
        else:
            self.invoke_export_datatable(datatable)
            # get the updated info every interval seconds until the data are available to a maximum of timeout seconds
            start = datetime.now()
            while (datetime.now() - start).seconds < timeout:
                info = self.get_datatable_info(datatable)
                if info.data.available:
                    return info.data.url
                sleep(interval)