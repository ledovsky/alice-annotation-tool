from os.path import join, exists

import pandas as pd
import numpy as np
import matplotlib
import tempfile

from django.test import TestCase, Client
from django.apps import apps

from main_app.vis import plot_topomap, plot_epochs_image, plot_spectrum
from main_app.models import ICAImages
from data_app.init_test_db import init_test_db
from data_app.models import ICAComponent


app_path = apps.get_app_config('data_app').path


class TestUpdatePlots(TestCase):
    temporary_dir = None

    def setUp(self):
        init_test_db()

    @classmethod
    def setUpClass(cls):
        cls.temporary_dir = tempfile.TemporaryDirectory(prefix='mediatest')
        super(TestUpdatePlots, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.temporary_dir = None
        super(TestUpdatePlots, cls).tearDownClass()

    def test_make_plots(self):
        print(self.temporary_dir.name)
        with self.settings(MEDIA_ROOT=self.temporary_dir.name):
            ICAImages.update_plots('test_dataset')
            ic = ICAComponent.objects.all()[0]
            assert exists(ic.x.get_image_path('topomap')) == True
            assert exists(ic.x.get_image_path('spectrum')) == True
            assert exists(ic.x.get_image_path('epochs_image')) == True


class TestComponentsPlot(TestCase):
    def setUp(self):
        init_test_db()

    def test_component_plot_view(self):
        client = Client()
        response = client.get('/api/view/subjects/components-plot/1')
        assert response.status_code == 200
        assert response.json()['subject_id'] == 1
        assert 'data' in response.json()['figure']
        assert 'layout' in response.json()['figure']