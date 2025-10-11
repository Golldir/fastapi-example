from faststream import FastStream
from faststream.kafka import KafkaBroker
import time
import asyncio
from src.app.core.metrics import metrics

broker = KafkaBroker("localhost:9092")
app = FastStream(broker)
    
@broker.subscriber("test-topic")
async def handle_msg(message: str):
    """Обработка сообщений из Kafka с метриками"""
    start_time = time.time()
    
    try:
        print(f"Получили: {message}")
        
        # Имитируем обработку заказа (2-5 секунд)
        processing_time = 2 + (hash(message) % 3)  # 2-5 секунд
        await asyncio.sleep(processing_time)
        
        # Записываем время обработки
        actual_duration = time.time() - start_time
        metrics.record_order_processing_time(actual_duration)
        
        print(f"Заказ обработан за {actual_duration:.2f} секунд")
        
    except Exception as e:
        print(f"Ошибка обработки заказа: {e}")
        raise e

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())   