from drf_backend.celery import app

from main_app.models import ICAImages, ICALinks


@app.task
def recalc_dataset(dataset_short_name):
    ICALinks.update_links(dataset_short_name)
    ICAImages.update_plots(dataset_short_name)
    