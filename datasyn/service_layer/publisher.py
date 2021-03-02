import json
from os import environ
from urllib.parse import urlunsplit

import click
import requests
from google.cloud import pubsub_v1

from datasyn.service_layer import synthesizer
from datasyn.settings import (
    DATCAT_HOST,
    DATCAT_PORT,
    DATCAT_SCHEME,
    GOOGLE_APPLICATION_CREDENTIALS,
    PROJECT_ID,
)

environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

DATCAT_NETLOC = f"{DATCAT_HOST}:{DATCAT_PORT}"
MAPPING_URL_COMPONENTS = (DATCAT_SCHEME, DATCAT_NETLOC, "/mappings", "", "")
MAPPING_URL = urlunsplit(MAPPING_URL_COMPONENTS)

batch_settings = pubsub_v1.types.BatchSettings(
    max_messages=10,  # default 100
    max_bytes=1024,  # default 1 MB
    max_latency=1,  # default 10 ms
)
publisher = pubsub_v1.PublisherClient()


def callback(future):
    message_id = future.result()
    print(message_id)


@click.command()
@click.option(
    "--number-of-messages",
    default=10,
    help="The number of synthetic messages a single request will publish",
)
@click.option(
    "--schema",
    help="A specific schema to use. Leave empty for a random selection from all schemas.",
)
def publish(number_of_messages: int, schema: str):
    response = requests.get(url=MAPPING_URL)
    mappings = response.json()

    if schema:
        mappings = {schema: mappings[schema]}

    for record in synthesizer.produce_synthetic_events(
        number_of_messages=number_of_messages, schema=schema
    ):

        topic = f'{record["event_name"]}_v{record["event_version"]}'
        topic_id = mappings[topic]["topic_name"]
        topic_path = publisher.topic_path(PROJECT_ID, topic_id)
        data = json.dumps(record).encode("utf-8")

        future = publisher.publish(topic_path, data)
        future.add_done_callback(callback)

    print(f"Published messages with error handler to {topic_path}")


if __name__ == "__main__":
    publish()
