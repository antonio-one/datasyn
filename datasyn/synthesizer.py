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
URL_COMPONENTS = (DATCAT_SCHEME, DATCAT_NETLOC, "/schemas", "", "")
URL = urlunsplit(URL_COMPONENTS)
TYPE_CALLABLE_MAPPING = {
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


def synthetic_event(schema: typing.List[typing.Dict[str, str]]):
    output = {}
    for field in schema:
        field_type = field["type"].lower()
        random_value = TYPE_CALLABLE_MAPPING[field_type]
        if random_value is None:
            raise ValueError(f"{random_value=} is not valid.")
        output[field["name"]] = random_value()
    return output


def produce_synthetic_events(number_of_messages: int):
    response = requests.get(url=URL)
    response.raise_for_status()
    schemas = response.json()
    if schemas == {}:
        raise InvalidSchema

    output = []
    while number_of_messages > 0:
        for schema in schemas.values():
            output.append(synthetic_event(schema=schema))
            number_of_messages -= 1
    return output


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
