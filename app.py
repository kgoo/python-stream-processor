import faust
from models import Event
from db import store_aggregate
from datetime import timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = faust.App(
    'event-aggregator',
    broker='kafka://localhost:9092',
    value_serializer='json',
    stream_wait_empty=True,
)

app.conf.stream_wait_empty = 1.0

event_topic = app.topic('events', value_type=Event)

agg_table = app.Table(
    'value_count_table',
    default=int,
    partitions=1,
    on_window_close=store_aggregate,
).tumbling(timedelta(seconds=10), expires=timedelta(minutes=1))

@app.agent(event_topic)
async def process(events):
    async for event in events:
        logger.info(f"Received event: {event}")
        agg_table[event.value] += 1
