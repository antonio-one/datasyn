from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from datasyn.service_layer.synthesizer import produce_synthetic_events

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse("/synthesizer/1")


@app.get("/synthesizer/{number_of_messages}")
async def messages(number_of_messages: int):
    synthetic_messages = produce_synthetic_events(number_of_messages=number_of_messages)
    return synthetic_messages
