from fuzzywuzzy import fuzz
import pytest
import operator


@pytest.mark.parametrize("fake_field_name, input_field_name, _operator, threshold", [
    ("first name", "first_name", operator.gt, 75),
    ("first name", "firstname", operator.gt, 75),
    ("last name", "last_name", operator.gt, 75),
    ("last name", "lastname", operator.gt, 75),
    ("home address", "email_address", operator.lt, 75),
    ("home address", "emailaddress", operator.lt, 75),
    ("homeaddress", "emailaddress", operator.lt, 75),
    ("office address", "email_address", operator.lt, 75),
    ("office address", "emailaddress", operator.lt, 75),
    ("officeaddress", "emailaddress", operator.lt, 75),
])
def test_high_threshold(fake_field_name: str, input_field_name: str, _operator: operator, threshold: int):
    assert _operator(fuzz.ratio(fake_field_name, input_field_name), threshold)
