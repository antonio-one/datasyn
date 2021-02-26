from os import getenv

import pytest
import vcr

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
from datasyn.service_layer.synthesizer import produce_synthetic_events

SCHEMA_URL = getenv("DATCAT_URL")


@pytest.mark.fast
@vcr.use_cassette("tests/vcr_cassettes/test_synthetic_messages.yaml")
def test_synthetic_messages():
    messages = produce_synthetic_events(schema_url=SCHEMA_URL, number_of_messages=11)
    expected_number_of_messages = 11
    assert len(messages) == expected_number_of_messages


@pytest.mark.fast
@pytest.mark.parametrize(
    ("datatype, function, expected"),
    [
        ("integer", random_integer, int),
        ("float", random_float, float),
        ("numeric", random_numeric, float),
        ("bignumeric", random_bignumeric, float),
        ("boolean", random_boolean, bool),
        ("string", random_string, str),
        ("bytes", random_bytes, str),
        ("date", random_date, str),
        ("datetime", random_datetime, str),
        ("time", random_time, str),
        ("timestamp", random_timestamp, float),
        ("geography", random_geography, str),
        ("record", random_record, str),
    ],
)
def test_type_to_callable(datatype: str, function: object, expected: type):
    assert isinstance(function(), expected)
