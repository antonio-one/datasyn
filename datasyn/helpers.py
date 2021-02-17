import typing
from datetime import datetime, time
from urllib.parse import urlunsplit
from uuid import uuid4

import requests
from numpy import random

from datasyn.settings import DATCAT_HOST, DATCAT_PORT, DATCAT_SCHEME

DATCAT_NETLOC = f"{DATCAT_HOST}:{DATCAT_PORT}"


class SyntheticEvent:
    # TODO: add random struct
    def __init__(self):
        self._new = {}

    @property
    def new(self):
        return self._new

    @new.setter
    def new(self, schema: typing.List[typing.Dict[str, str]]):
        for field in schema:
            field_type = field["type"].lower()
            random_value = self.type_callable_mapping[field_type]
            self._new[field["name"]] = random_value()

    @property
    def type_callable_mapping(self) -> typing.Dict[str, callable]:
        return {
            "integer": self.random_integer,
            "float": self.random_float,
            "numeric": self.random_numeric,
            "bignumeric": self.random_bignumeric,
            "boolean": self.random_boolean,
            "string": self.random_string,
            "bytes": self.random_bytes,
            "date": self.random_date,
            "datetime": self.random_datetime,
            "time": self.random_time,
            "timestamp": self.random_timestamp,
            "geography": self.random_geography,
        }

    def random_integer(self) -> int:
        return random.randint(-9223372036854775808, 9223372036854775808)

    def random_float(self) -> float:
        return random.uniform(-9223372036854775808, 9223372036854775808)

    def random_numeric(self) -> float:
        # TODO: precision and scale
        return random.uniform(-9223372036854775808, 9223372036854775808)

    def random_bignumeric(self) -> float:
        # TODO: precision and scale
        return random.uniform(-9223372036854775808, 9223372036854775808)

    def random_boolean(self) -> bool:
        return f"{random.choice([True, False])}"

    def random_string(self) -> str:
        return str(uuid4())

    def random_bytes(self) -> bytes:
        return random.bytes(16)

    def random_date(self) -> datetime:
        return datetime.date(datetime.now())

    def random_datetime(self) -> datetime:
        return datetime.now()

    def random_time(self) -> time:
        return datetime.time(datetime.now())

    def random_timestamp(self) -> float:
        return float(datetime.timestamp(datetime.now()))

    def random_geography(self) -> str:
        longitude = random.randint(-180, 180)
        latitude = random.randint(-90, 90)
        return f"ST_GEOGPOINT({longitude}, {latitude})"


def produce_synthetic_events():
    url_components = (DATCAT_SCHEME, DATCAT_NETLOC, "/schemas", "", "")
    url = urlunsplit(url_components)
    response = requests.get(url=url)
    response.raise_for_status()
    schemas = response.json()

    for _, schema in schemas.items():
        se = SyntheticEvent()
        se.new = schema
        print(se.new)
        breakpoint()


def main():
    produce_synthetic_events()


if __name__ == "__main__":
    main()
