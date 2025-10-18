from faststream.kafka import KafkaBroker
import asyncio

broker = KafkaBroker("localhost:9092")

async def send_hello():
    async with broker:
        await broker.publish("hello", topic="test-topic")
        print("Отправили: hello")

if __name__ == "__main__":
    asyncio.run(send_hello())
