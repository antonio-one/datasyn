__all__ = [
    "random_integer",
    "random_float",
    "random_numeric",
    "random_bignumeric",
    "random_boolean",
    "random_string",
    "random_bytes",
    "random_date",
    "random_datetime",
    "random_time",
    "random_timestamp",
    "random_geography",
    "random_struct",
    "random_record",
]

import base64
from datetime import datetime
from uuid import uuid4

from numpy import random

MIN_INT, MAX_INT = -9223372036854775808, 9223372036854775808


def random_integer() -> int:
    return random.randint(MIN_INT, MAX_INT)


def random_float() -> float:
    return random.uniform(MIN_INT, MAX_INT)


def random_numeric() -> float:
    # TODO: precision and scale
    return random.uniform(MIN_INT, MAX_INT)


def random_bignumeric() -> float:
    # TODO: precision and scale
    return random.uniform(MIN_INT, MAX_INT)


def random_boolean() -> str:
    return f"{random.choice([True, False])}".lower()


def random_string() -> str:
    return str(uuid4())


def random_bytes() -> bytes:
    encoded = base64.b64encode(random.bytes(16))
    return encoded.decode("ascii")


def random_date() -> str:
    return str(datetime.date(datetime.now()))


def random_datetime() -> str:
    return str(datetime.now())


def random_time() -> str:
    return str(datetime.time(datetime.now()))


def random_timestamp() -> float:
    return float(datetime.timestamp(datetime.now()))


def random_geography() -> str:
    longitude = random.randint(-180, 180)
    latitude = random.randint(-90, 90)
    return f"POINT({longitude} {latitude})"


def random_struct() -> str:
    # TODO: decide whether to support legacy sql
    return ""


def random_record() -> str:
    # TODO: decide whether to support legacy sql
    return ""