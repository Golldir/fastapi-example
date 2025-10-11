from prometheus_client import Counter, generate_latest


class MetricsCollector:
    """Минимальный класс для метрик Prometheus"""
    
    def __init__(self):
        # Счетчик заказов
        self.orders_total = Counter('orders_total', 'Количество заказов')
    
    def increment_orders(self):
        """Увеличить счетчик заказов"""
        self.orders_total.inc()
    
    def get_metrics(self) -> str:
        """Получить метрики"""
        return generate_latest().decode('utf-8')
    
    def set_database_status(self, status: bool):
        """Установить статус подключения к базе данных"""
        self.database_status.set(status)


# Глобальный экземпляр
metrics = MetricsCollector()
