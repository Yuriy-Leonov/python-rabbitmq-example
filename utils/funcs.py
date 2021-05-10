from utils import connector


async def declare_queue(queue_name, durable=False):
    conct = connector.Connector()
    channel = await conct.get_channel()
    await channel.queue_declare(
        queue=queue_name,
        durable=durable,
    )
