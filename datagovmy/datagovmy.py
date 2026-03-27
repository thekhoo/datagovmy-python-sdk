from typing import Optional

from datagovmy.service import DataCatalogueClient, OpenDOSMClient


class DataGovMyClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._data_catalogue: Optional[DataCatalogueClient] = None
        self._opendosm: Optional[OpenDOSMClient] = None

    @property
    def data_catalogue(self) -> DataCatalogueClient:
        if self._data_catalogue is None:
            self._data_catalogue = DataCatalogueClient(api_key=self.api_key)
        return self._data_catalogue

    @property
    def opendosm(self) -> OpenDOSMClient:
        if self._opendosm is None:
            self._opendosm = OpenDOSMClient(api_key=self.api_key)
        return self._opendosm
