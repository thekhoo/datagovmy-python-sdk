from datagovmy.service.data_endpoint import DataEndpointClient


class DataCatalogueClient(DataEndpointClient):
    ENDPOINT = "/data-catalogue"
