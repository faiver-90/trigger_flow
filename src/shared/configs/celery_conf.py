# src/shared/configs/celery_conf.py
from kombu import Exchange, Queue

from src.shared.configs.get_settings import get_settings

settings = get_settings()

# --- Брокер и бэкенд ---
broker_url = settings.celery_broker_url
result_backend = settings.celery_result_backend
result_backend_transport_options = {"retry_on_timeout": True}

# --- Сериализация/таймзона ---
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

# --- Надёжность/поведение ---
task_acks_late = True
task_reject_on_worker_lost = True
task_acks_on_failure_or_timeout = True
broker_pool_limit = 10
broker_heartbeat = 30
broker_connection_retry_on_startup = True
broker_connection_max_retries = 100
broker_transport_options = {"visibility_timeout": 3600}

# --- Exchanges и очереди ---
default_ex = Exchange("default", type="direct", durable=True)
notify_ex = Exchange("notify", type="direct", durable=True)

task_default_queue = "default"
task_queues = (
    Queue("default", exchange=default_ex, routing_key="default", durable=True),
    Queue("notify_email", exchange=notify_ex, routing_key="notify.email", durable=True),
    Queue("notify_tg", exchange=notify_ex, routing_key="notify.tg", durable=True),
    Queue("notify_sms", exchange=notify_ex, routing_key="notify.sms", durable=True),
)

# --- Роутинг по имени задачи ---
task_routes = {
    "src.shared.celery_module.tasks.notify_email": {
        "queue": "notify_email",
        "routing_key": "notify.email",
    },
    "src.shared.celery_module.tasks.notify_tg": {
        "queue": "notify_tg",
        "routing_key": "notify.tg",
    },
    "src.shared.celery_module.tasks.notify_sms": {
        "queue": "notify_sms",
        "routing_key": "notify.sms",
    },
}

# --- Пример beat-расписания (опционально) ---
# beat_schedule = {
#     "cleanup-every-night": {
#         "task": "src.shared.celery_module.tasks.cleanup",
#         "schedule": crontab(hour=2, minute=0),
#     },
# }
