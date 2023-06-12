from django.core.management.base import BaseCommand
from main_app.models import DatasetStats

class Command(BaseCommand):
    def handle(self, *args, **options):
        DatasetStats.update_stats()
