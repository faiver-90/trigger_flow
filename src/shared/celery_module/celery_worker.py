from celery import Celery

from src.shared.configs import celery_conf


def get_celery_app() -> Celery:
    """Создать и настроить экземпляр Celery."""
    celery_inst = Celery("celery_service")
    celery_inst.config_from_object(celery_conf)
    celery_inst.autodiscover_tasks(packages=["src.shared.celery_module.tasks"])

    return celery_inst


celery_app = get_celery_app()
