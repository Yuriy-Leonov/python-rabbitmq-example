import asyncio

from utils import connector
from utils import funcs

ROUTING_KEY_1 = "*.one.*"
ROUTING_KEY_2 = "*.two.*"
ROUTING_KEY_3 = "*.three.*"
ROUTING_KEY_4 = "huge.*"

EXCHANGE_NAME = "simple_topic_exchange"

QUEUE_NAME_1 = "example_topic_exchange_1"
QUEUE_NAME_2 = "example_topic_exchange_2"
QUEUE_NAME_3 = "example_topic_exchange_3"
QUEUE_NAME_4 = "example_topic_exchange_4"


async def send_message_with_shared_channel():
    conct = connector.Connector()
    shared_channel = await conct.get_channel()
    await shared_channel.basic_publish(
        b"Some text",
        exchange=EXCHANGE_NAME,
        routing_key="huge.one"
    )


async def main():
    await funcs.declare_queue(queue_name=QUEUE_NAME_1)
    await funcs.declare_queue(queue_name=QUEUE_NAME_2)
    await funcs.declare_queue(queue_name=QUEUE_NAME_3)
    await funcs.declare_queue(queue_name=QUEUE_NAME_4)
    await funcs.declare_exchange(
        exchange_name=EXCHANGE_NAME,
        exchange_type="topic",
    )
    await funcs.bind_queue(
        queue_name=QUEUE_NAME_1,
        exchange_name=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_1
    )
    await funcs.bind_queue(
        queue_name=QUEUE_NAME_2,
        exchange_name=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_2
    )
    await funcs.bind_queue(
        queue_name=QUEUE_NAME_3,
        exchange_name=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_3
    )
    await funcs.bind_queue(
        queue_name=QUEUE_NAME_4,
        exchange_name=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_4
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
