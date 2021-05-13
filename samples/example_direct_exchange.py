import asyncio

from utils import connector
from utils import funcs

QUEUE_NAME_GREEN = "example_direct_exchange_green"
ROUTING_KEY = "green"
EXCHANGE_NAME = "simple_direct_exchange"
QUEUE_NAME_RED = "example_direct_exchange_red"
QUEUE_NAME_BLUE = "example_direct_exchange_blue"


async def send_message_with_shared_channel():
    conct = connector.Connector()
    shared_channel = await conct.get_channel()
    await shared_channel.basic_publish(
        b"Some text",
        routing_key=QUEUE_NAME_GREEN
    )


async def main():
    await funcs.declare_queue(queue_name=QUEUE_NAME_GREEN)
    await funcs.declare_queue(queue_name=QUEUE_NAME_RED)
    await funcs.declare_queue(queue_name=QUEUE_NAME_BLUE)
    await funcs.declare_exchange(
        exchange_name=EXCHANGE_NAME,
        exchange_type="direct",
    )
    await funcs.bind_queue(
        queue_name=QUEUE_NAME_GREEN,
        exchange_name=EXCHANGE_NAME,
        routing_key=ROUTING_KEY
    )
    await funcs.bind_queue(
        queue_name=QUEUE_NAME_RED,
        exchange_name=EXCHANGE_NAME,
        routing_key="red"
    )
    await funcs.bind_queue(
        queue_name=QUEUE_NAME_BLUE,
        exchange_name=EXCHANGE_NAME,
        routing_key="blue"
    )

    await send_message_with_shared_channel()

    # close connection
    conct = connector.Connector()
    conn = await conct.get_connection()
    await conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
