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
SCHEMA_URL_COMPONENTS = (DATCAT_SCHEME, DATCAT_NETLOC, "/schemas", "", "")
SCHEMA_URL = urlunsplit(SCHEMA_URL_COMPONENTS)

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
        random_value = TYPE_TO_CALLABLE[field_type]

        if random_value is None:
            raise ValueError(f"{random_value=} is not valid.")
        if field["name"] == "event_datetime":
            se[field["name"]] = random_datetime()
        elif field["name"] == "event_name":
            se[field["name"]] = schema_class
        elif field["name"] == "event_version":
            se[field["name"]] = schema_version
        else:
            se[field["name"]] = random_value()
    return se


def produce_synthetic_events(number_of_messages: int):

    response = requests.get(url=SCHEMA_URL)
    response.raise_for_status()
    schemas = response.json()
    if schemas == {}:
        raise InvalidSchema

    records = []
    while True:

        for schema_name, fields in schemas.items():

            schema_class, schema_version = schema_name.split("_v")
            record = synthetic_event(
                schema_class=schema_class,
                schema_version=int(schema_version),
                fields=fields,
            )
            records.append(record)

            number_of_messages -= 1
            if number_of_messages <= 0:
                return records


@click.command()
@click.option(
    "--number-of-messages",
    default=100,
    help="The number of synthetic messages a single request will return",
)
def main(number_of_messages: int):
    produce_synthetic_events(number_of_messages)


if __name__ == "__main__":
    main()
