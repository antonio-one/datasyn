import typing
from datetime import date, datetime, time

import pytest


@pytest.mark.parametrize(
    "schema, expected_type",
    [
        (
            [
                {
                    "description": "",
                    "mode": "REQUIRED",
                    "name": "COL1",
                    "type": "INTEGER",
                }
            ],
            int,
        ),
        (
            [{"description": "", "mode": "REQUIRED", "name": "COL1", "type": "FLOAT"}],
            float,
        ),
        (
            [
                {
                    "description": "",
                    "mode": "REQUIRED",
                    "name": "COL1",
                    "type": "NUMERIC",
                }
            ],
            float,
        ),
        (
            [
                {
                    "description": "",
                    "mode": "REQUIRED",
                    "name": "COL1",
                    "type": "BIGNUMERIC",
                }
            ],
            float,
        ),
        # ([{"description": "", "mode": "REQUIRED", "name": "COL1", "type": "BOOLEAN"}], bool),
        (
            [{"description": "", "mode": "REQUIRED", "name": "COL1", "type": "STRING"}],
            str,
        ),
        (
            [{"description": "", "mode": "REQUIRED", "name": "COL1", "type": "BYTES"}],
            bytes,
        ),
        (
            [{"description": "", "mode": "REQUIRED", "name": "COL1", "type": "DATE"}],
            date,
        ),
        (
            [
                {
                    "description": "",
                    "mode": "REQUIRED",
                    "name": "COL1",
                    "type": "DATETIME",
                }
            ],
            datetime,
        ),
        (
            [{"description": "", "mode": "REQUIRED", "name": "COL1", "type": "TIME"}],
            time,
        ),
        (
            [
                {
                    "description": "",
                    "mode": "REQUIRED",
                    "name": "COL1",
                    "type": "TIMESTAMP",
                }
            ],
            float,
        ),
        (
            [
                {
                    "description": "",
                    "mode": "REQUIRED",
                    "name": "COL1",
                    "type": "GEOGRAPHY",
                }
            ],
            str,
        ),
    ],
)
def test_new_simple_event(
    schema: typing.List[typing.Dict[str, typing.Any]], expected_type: type
):
    # TODO: make boolean work
    return
