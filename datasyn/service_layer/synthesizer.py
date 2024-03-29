import typing
from urllib.parse import urlunsplit

import click
import requests
from requests.exceptions import InvalidSchema

from datasyn.helpers import (
    random_bignumeric,
    random_boolean,
    random_bytes,
    random_date,
    random_datetime,
    random_float,
    random_geography,
    random_integer,
    random_numeric,
    random_record,
    random_string,
    random_time,
    random_timestamp,
)
from datasyn.settings import DATCAT_HOST, DATCAT_PORT, DATCAT_SCHEME

DATCAT_NETLOC = f"{DATCAT_HOST}:{DATCAT_PORT}"
SCHEMA_URL_COMPONENTS = (DATCAT_SCHEME, DATCAT_NETLOC, "v1/datcat/schemas/list/refresh/true", "", "")
SCHEMA_CATALOGUE_URL = urlunsplit(SCHEMA_URL_COMPONENTS)

TYPE_TO_CALLABLE = {
    "integer": random_integer,
    "float": random_float,
    "numeric": random_numeric,
    "bignumeric": random_bignumeric,
    "boolean": random_boolean,
    "string": random_string,
    "bytes": random_bytes,
    "date": random_date,
    "datetime": random_datetime,
    "time": random_time,
    "timestamp": random_timestamp,
    "geography": random_geography,
    "record": random_record,
}


def synthetic_event(
    schema_class: str, schema_version: int, fields: typing.List[typing.Dict[str, str]]
):
    se = {}

    for field in fields:
        field_type = field["type"].lower()
        _callable = TYPE_TO_CALLABLE[field_type]
        if field_type == "string":
            random_value = _callable(column_name=field["name"])
        else:
            random_value = _callable()

        if random_value is None:
            raise ValueError(f"{random_value=} is not valid.")
        if field["name"] == "event_datetime":
            se[field["name"]] = random_datetime()
        elif field["name"] == "event_name":
            se[field["name"]] = schema_class
        elif field["name"] == "event_version":
            se[field["name"]] = schema_version
        else:
            se[field["name"]] = random_value
    return se


def produce_synthetic_events(
    schema: typing.Dict[str, typing.Dict],
    schema_catalogue_url: str = SCHEMA_CATALOGUE_URL,
    number_of_messages: int = 1,
):

    response = requests.get(url=schema_catalogue_url)
    response.raise_for_status()
    schemas = response.json()
    if schemas == {}:
        raise InvalidSchema

    if schema:
        schemas = {schema: schemas[schema]}

    records = []
    count = 0
    while True:

        for schema_name, fields in schemas.items():

            schema_class, schema_version = schema_name.split("_v")
            record = synthetic_event(
                schema_class=schema_class,
                schema_version=int(schema_version),
                fields=fields,
            )
            records.append(record)

            count += 1
            if count == number_of_messages:
                return records


@click.command()
@click.option(
    "--schema-url", default=SCHEMA_CATALOGUE_URL, help="The url of the data catalogue"
)
@click.option(
    "--number-of-messages",
    default=10,
    help="The number of synthetic messages a single request will return",
)
def main(schema_url: str, number_of_messages: int):
    produce_synthetic_events(schema_url, number_of_messages)


if __name__ == "__main__":
    main()
