import os
import shutil
import subprocess
from os.path import join, exists

import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings

from data_app.models import Dataset, ICAComponent, ICAData, Annotation
from data_app.downloads import create_ics, create_annotations_raw, create_components_data_iter
from downloads_app.utils import get_dirname


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

        dir_name = get_dirname(dataset_short_name, options['ds_version'])
        out_dir = join(settings.OUT_DIR, dir_name)

        if exists(out_dir):
            shutil.rmtree(out_dir, ignore_errors=True)
        os.mkdir(out_dir)

        # create ics.csv
        df_ics = create_ics(dataset_short_name)
        df_ics.to_csv(join(out_dir, 'ics.csv'), index=False)

        # create annotations_raw.csv

        df_annotations_raw = create_annotations_raw(dataset_short_name)
        df_annotations_raw.to_csv(join(out_dir, 'annotations_raw.csv'), index=False)


        # create components data
        for ic_id, df_ica_weights, df_ica_data in create_components_data_iter(dataset_short_name):
            df_ica_weights.to_csv(join(out_dir, ic_id + '_weights.csv'), index=False)
            df_ica_data.to_csv(join(out_dir, ic_id + '_data.csv'), index=False)

        proc = subprocess.Popen(['zip', '-r', dir_name + '.zip', dir_name], cwd=settings.OUT_DIR)
        proc.communicate()
