import asyncio
import json
import time

from utils import connector
from utils import funcs

QUEUE_NAME = "example_with_individual_channel"
i = 0


async def send_message_with_shared_channel():
    global i
    conct = connector.Connector()
    conn = await conct.get_connection()
    individual_channel = await conn.channel()
    await individual_channel.basic_publish(
        body=json.dumps({
            "some": "obj"
        }).encode(),
        routing_key=QUEUE_NAME
    )
    i += 1
    # print(f"finish. total = {i}")


async def main():
    await funcs.declare_queue(queue_name=QUEUE_NAME)
    tasks = [
        send_message_with_shared_channel()
        for _ in range(10000)
    ]
    await asyncio.gather(*tasks)
    # close connection
    conct = connector.Connector()
    conn = await conct.get_connection()
    await conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start = time.time()
    loop.run_until_complete(main())
    print(f"time execution: {time.time() - start:.2f} sec")
    loop.close()
