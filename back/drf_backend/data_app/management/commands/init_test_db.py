from django.core.management.base import BaseCommand

from data_app.init_test_db import init_test_db


class Command(BaseCommand):

    def handle(self, *args, **options):
        init_test_db()