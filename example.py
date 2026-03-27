import logging

from datagovmy import DataGovMyClient


def main():
    client = DataGovMyClient()
    data = client.data_catalogue.get_dataset_as_json(id="population_malaysia")
    print(data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
