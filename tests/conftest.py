import pytest


@pytest.fixture(scope="module")
def vcr_config():
    """VCR.py registers full request and response, including headers, which often include passwords or API keys.
    It's important to make sure you aren't leaving any secrets in your cassettes.
    https://pytest-vcr.readthedocs.io/en/latest/#filtering-saved-requestresponse
    """
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("authorization", "DUMMY")],
    }
