import json
from pathlib import Path

from faststream import FastStream
from faststream.redis import RedisBroker

from .settings import settings

broker = RedisBroker(settings.redis_url)
app = FastStream(broker)

LOG_PATH = Path("data/logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_PATH / "predictions.jsonl"


@broker.subscriber("prediction_events")
async def handle_message(msg: dict):
    try:
        obj = msg
    except Exception as err:
        print('Error:', err)
        return

    with LOG_FILE.open("a", encoding="utf8") as f:
        f.write(json.dumps(obj) + "\n")

    print("saved:", obj)


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
