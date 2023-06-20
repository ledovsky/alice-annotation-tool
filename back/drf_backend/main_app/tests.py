from os.path import join, exists

import pandas as pd
import numpy as np
import tempfile

from django.test import TestCase, Client
from django.apps import apps

from data_app.init_test_db import init_test_db
from data_app.models import ICAComponent, Subject
from .tasks import update_ic_plots, update_links, update_dataset_stats


app_path = apps.get_app_config('data_app').path


class TestUpdateICPlots(TestCase):
    temporary_dir = None

    def setUp(self):
        init_test_db()

    @classmethod
    def setUpClass(cls):
        cls.temporary_dir = tempfile.TemporaryDirectory(prefix='mediatest')
        super(TestUpdateICPlots, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.temporary_dir = None
        super(TestUpdateICPlots, cls).tearDownClass()

    def test_make_plots(self):
        print(self.temporary_dir.name)
        with self.settings(MEDIA_ROOT=self.temporary_dir.name):
            update_ic_plots('test_dataset')


class TestComponentsPlot(TestCase):
    def setUp(self):
        init_test_db()

    def test_component_plot_view(self):
        client = Client()
        subject_id = Subject.objects.all()[0].id
        response = client.get(f'/api/view/subjects/components-plot/{subject_id}')
        assert response.status_code == 200
        assert response.json()['subject_id'] == subject_id
        assert 'data' in response.json()['figure']
        assert 'layout' in response.json()['figure']


class TestComponentsPlotNpy(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_dir = tempfile.TemporaryDirectory(prefix='mediatest')
        super(TestComponentsPlotNpy, cls).setUpClass()

    def setUp(self):
        init_test_db()
        with self.settings(MEDIA_ROOT=self.temporary_dir.name):
            subjects = Subject.objects.all()
            for subject in subjects:
                subject.create_npy()

    def test_component_plot_view(self):
        with self.settings(MEDIA_ROOT=self.temporary_dir.name):
            client = Client()
            subject_id = Subject.objects.all()[0].id
            response = client.get(f'/api/view/subjects/components-plot/{subject_id}')
            assert response.status_code == 200
            assert response.json()['subject_id'] == subject_id
            assert 'data' in response.json()['figure']
            assert 'layout' in response.json()['figure']


class TestUpdateLinks(TestCase):
    def setUp(self):
        init_test_db()

    def test_component_plot_view(self):
        update_links('test_dataset')
        ics = ICAComponent.objects.filter(subject__name='S7').order_by('name')
        assert ics[1].x.prev is not None
        assert ics[1].x.next is not None


class TestUpdateDatasetStats(TestCase):
    def setUp(self):
        init_test_db()

    def test_update_dataset_stats(self):
        update_dataset_stats()