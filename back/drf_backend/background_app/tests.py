import tempfile

from django.test import TestCase, Client
from django.urls import reverse

from data_app.models import Dataset, ICAComponent
from data_app.init_test_db import init_test_db
from .models import BackgroundTask
from .tasks import update_links, update_dataset_stats, update_ic_plots


## Test views

class TestRunDatasetBackgroudTaskView(TestCase):
    temporary_dir = None

    def setUp(self) -> None:
        init_test_db()

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_dir = tempfile.TemporaryDirectory(prefix='mediatest')
        super(TestRunDatasetBackgroudTaskView, cls).setUpClass()

    def test_dataset_view_list(self) -> None:
        client = Client()
        client.login(username='admin', password='admin')
        with self.settings(
            MEDIA_ROOT=self.temporary_dir.name,
            CELERY_TASK_ALWAYS_EAGER=True,
        ):
            dataset_id = Dataset.objects.all()[0].id
            data = {'dataset_id': dataset_id, 'task_name': 'update-links'}
            response = client.post(reverse('background-run-dataset'), data=data)
            assert response.status_code == 200

            data = {'dataset_id': dataset_id, 'task_name': 'update-ic-plots'}
            response = client.post(reverse('background-run-dataset'), data=data)
            assert response.status_code == 200

            background_tasks = BackgroundTask.objects.all()
            assert len(background_tasks) == 2
            assert background_tasks[0].status == 'success'
            assert background_tasks[1].status == 'success'


class TestRunBackgroudTaskView(TestCase):
    temporary_dir = None

    def setUp(self) -> None:
        init_test_db()

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_dir = tempfile.TemporaryDirectory(prefix='mediatest')
        super(TestRunBackgroudTaskView, cls).setUpClass()

    def test_dataset_view_list(self) -> None:
        client = Client()
        client.login(username='admin', password='admin')
        with self.settings(
            MEDIA_ROOT=self.temporary_dir.name,
            CELERY_TASK_ALWAYS_EAGER=True,
        ):
            data = {'task_name': 'update-dataset-stats'}
            response = client.post(reverse('background-run'), data=data)
            assert response.status_code == 200

            background_tasks = BackgroundTask.objects.all()
            assert len(background_tasks) == 1
            assert background_tasks[0].status == 'success'

            data = {'task_name': 'some-wrong-task'}
            response = client.post(reverse('background-run'), data=data)
            assert response.status_code == 400


class TestBackgroundTaskView(TestCase):
    def setUp(self) -> None:
        init_test_db()
    
    def test_backround_task_list(self) -> None:
        update_links('test_dataset')
        client = Client()
        response = client.get(reverse('background-list'))
        assert response.status_code == 200
        assert len(response.json()) == 1


## Test tasks

class TestUpdateLinks(TestCase):
    def setUp(self) -> None:
        init_test_db()

    def test_component_plot_view(self) -> None:
        update_links('test_dataset')
        ics = ICAComponent.objects.filter(subject__name='S7').order_by('name')
        assert ics[1].x.prev is not None
        assert ics[1].x.next is not None
        background_tasks = BackgroundTask.objects.all()
        assert len(background_tasks) == 1
        assert background_tasks[0].status == 'success'


class TestUpdateDatasetStats(TestCase):
    def setUp(self) -> None:
        init_test_db()

    def test_update_dataset_stats(self) -> None:
        update_dataset_stats()
        background_tasks = BackgroundTask.objects.all()
        assert len(background_tasks) == 1
        assert background_tasks[0].status == 'success'
