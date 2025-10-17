from prometheus_client import Counter, Gauge

ORDERS_TOTAL = Counter(
    "orders_total", 
    "Количество заказов"
)
DB_STATUS = Gauge(
    "database_connection_status", 
    "Статус подключения к базе данных", 
    ["db"]
)            

