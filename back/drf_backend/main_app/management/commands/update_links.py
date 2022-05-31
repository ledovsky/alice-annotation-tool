from django.core.management.base import BaseCommand
from main_app.models import ICAImages, ICALinks


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named arguments
        parser.add_argument(
            '--dataset',
            action='store',
            required=True,
            help='',
        )

    def handle(self, *args, **options):
        dataset_short_name = options['dataset']
        ICALinks.update_links(dataset_short_name)
