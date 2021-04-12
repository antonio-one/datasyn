from fuzzywuzzy import fuzz


def test_first_name():
    assert fuzz.ratio("first name", "first_name") > 75