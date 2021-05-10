import asyncio
import datetime
import time

from aiormq import spec

from utils import connector
from utils import funcs

QUEUE_NAME = "example_message_attributes"


async def send_message_with_shared_channel():
    global i
    conct = connector.Connector()
    shared_channel = await conct.get_channel()

    result = await shared_channel.basic_publish(
        body=b"Some bytes",
        routing_key=QUEUE_NAME,
        exchange="",  # empty mean default

        mandatory=False,
        # The mandatory flag tells RabbitMq that the message must be routable.,
        # that is, there must be one or more bound queues that will
        # receive the message
        #
        # raises exception if there is no target queue

        immediate=False,
        # checks: does target queue have consumer
        # if not - raises exception

        properties=spec.Basic.Properties(
            content_type="application/json",
            # no default behavior, it's only your agreement

            content_encoding="gzip",
            # no default behavior, it's only your agreement

            headers={
                "any": "thing",
                "you": "want"
            },

            delivery_mode=2,
            # 1 is default
            # 1 - will be deleted from queue in case service restart
            # 2 - will be kept in queue in case service restart

            priority=1,
            # just skip it
            # https://www.rabbitmq.com/priority.html

            expiration="10000",
            # 10 sec, value in miliseconds
            # https://www.rabbitmq.com/ttl.html#per-message-ttl-in-publishers

            user_id="guest",
            # https://www.rabbitmq.com/validated-user-id.html

            timestamp=datetime.datetime.now(),
            # just timestamp

            correlation_id="any string across all you system",
            # no default behavior, it's only your agreement

            message_id="your id",
            # no default behavior, it's only your agreement

            message_type="request/response/error",
            # no default behavior, it's only your agreement

            reply_to="callback_queue_name",
            # no default behavior, it's only your agreement

            app_id="any you want",
            # no default behavior, it's only your agreement
        ),
    )
    print(result)


async def main():
    await funcs.declare_queue(queue_name=QUEUE_NAME, durable=False)
    await send_message_with_shared_channel()
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
