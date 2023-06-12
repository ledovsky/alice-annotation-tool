from os.path import join, exists, basename

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

from data_app.models import Dataset
from downloads_app.models import DatasetDownloadItem
from downloads_app.utils import get_archive_name


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named arguments
        parser.add_argument(
            '--dataset',
            action='store',
            required=True,
            help='Dataset short name',
        )

        parser.add_argument(
            '--ds-version',
            action='store',
            required=False,
            default=None,
            help='Version of the dataset',
        )

    def handle(self, *args, **options):

        dataset_short_name = options['dataset']

        version = None
        if options['ds_version']:
            version = options['ds_version']
        
        file_path = get_archive_name(dataset_short_name, version)
        path = join(settings.OUT_DIR, file_path)

        if not exists(path):
            raise ValueError('File does not exists')

        dataset = Dataset.objects.get(short_name=dataset_short_name)

        download_item = DatasetDownloadItem(dataset=dataset, version=version)
        with open(path, 'rb') as f:
            download_item.file = File(f, name=basename(f.name))
            download_item.save()
