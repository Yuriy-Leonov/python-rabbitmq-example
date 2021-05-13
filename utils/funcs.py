from utils import connector


async def declare_queue(queue_name, durable=False):
    conct = connector.Connector()
    channel = await conct.get_channel()
    await channel.queue_declare(
        queue=queue_name,
        durable=durable,
    )


async def bind_queue(queue_name, exchange_name, routing_key):
    conct = connector.Connector()
    channel = await conct.get_channel()
    await channel.queue_bind(
        queue=queue_name,
        exchange=exchange_name,
        routing_key=routing_key,
    )


async def declare_exchange(
        exchange_name,
        exchange_type="direct",
        durable=False,
):
    conct = connector.Connector()
    channel = await conct.get_channel()
    await channel.exchange_declare(
        exchange=exchange_name,
        exchange_type=exchange_type,
        durable=durable,

        passive=False,
        # if passive is True - it will raise exception if exchange
        # doesn't exist

        internal=False,
        # If set, the exchange may not be used directly by publishers,
        # but only when bound to other exchanges. Internal exchanges are
        # used to construct wiring that is not visible to applications.
        # Hint: could be used as "dead-letter-exchange" for queues
    )

