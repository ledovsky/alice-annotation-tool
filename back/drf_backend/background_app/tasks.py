from typing import Callable

from drf_backend.utils import bot_send
from data_app.models import ICAComponent

from main_app.models import ICExtended, DatasetStats
from .celery import app
from .models import BackgroundTask



def celery_task_inner(task_name: str, details: str, callable: Callable):
    """Logging and error handling"""
    celery_log = BackgroundTask(task=task_name, details=details, status='in progress')
    celery_log.save()
    try:
        callable()
        celery_log.status = 'success'
    except Exception as e:
        celery_log.status = 'failed'
        message = f'Failed Celery job {task_name}\n{e.args[0]}'
        print(message)
        bot_send(message)
        celery_log.status = 'failed'
    finally:
        celery_log.save()


@app.task
def update_ic_plots(dataset_short_name: str) -> None:
    task_name = 'update-ic-plots'
    details = f'dataset: {dataset_short_name}'
    def callable():
        ics = ICAComponent.objects.all()
        if dataset_short_name:
            ics = ics.filter(dataset__short_name=dataset_short_name)

        for ic in ics:
            ic_x = ICExtended.get_or_create(ic.id)
            ic_x.update_plots()
    
    celery_task_inner(task_name, details, callable)


@app.task
def update_links(dataset_short_name: str) -> None:
    task_name = 'update-links'
    details = f'dataset: {dataset_short_name}'
    def callable():
        ICExtended.update_links(dataset_short_name)
    celery_task_inner(task_name, details, callable)


@app.task(name='update-dataset-stats')
def update_dataset_stats() -> None:
    task_name = 'update-dataset-stats'
    details = ''
    def callable():
        DatasetStats.update_stats()
    celery_task_inner(task_name, details, callable)