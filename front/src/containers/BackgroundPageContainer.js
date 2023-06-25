import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { BackgroundPage } from "../components/BackgroundPage";
import Api from '../api';


function BackgroundPageContainer (props) {

  const datasetTaskOptions = [
    {
        name: 'Update plots',
        value: 'update-ic-plots'
    },
    {
        name: 'Update links',
        value: 'update-links'
    },
  ];
  const generalTaskOptions = [
    {
        name: 'Update dataset stats',
        value: 'update-dataset-stats'
    },
  ];
  const [ datasets, setDatasets ] = useState([]);
  const [ selectedDatasetTask, setSelectedDatasetTask ] = useState(datasetTaskOptions[0].value);
  const [ selectedGeneralTask, setSelectedGeneralTask ] = useState(generalTaskOptions[0].value);
  const [ selectedDataset, setSelectedDataset ] = useState(-1);
  const [ tasks, setTasks ] = useState([]);

  useEffect(() => {
    async function fetchData() {
      let _datasets = await Api.getList('view/datasets/list', {});
      setDatasets(_datasets);
      setSelectedDataset(_datasets[0].id);
      let _tasks = await Api.getJson('background/list', {limit: 30});
      setTasks(_tasks.results);
    }
    fetchData();
  }, []);

  async function onSelectDataset(e) {
    setSelectedDataset(e.target.value);
  }

  async function onSelectDatasetTask(e) {
    setSelectedDatasetTask(e.target.value);
  }

  async function onSelectGeneralTask(e) {
    setSelectedGeneralTask(e.target.value);
  }

  async function onSubmitDatasetTask() {
    let response = await Api.post(`background/run-dataset`, {dataset_id: selectedDataset, task_name: selectedDatasetTask});
    let data = await response.json();
    if (data.status == 'ok') {
        toast.success('Task successfully started');
    } else {
        toast.error('Something has gone wrong');
    }
  }

  async function onSubmitGeneralTask() {
    let response = await Api.post(`background/run`, {task_name: selectedGeneralTask});
    let data = await response.json();
    if (data.status == 'ok') {
        toast.success('Task successfully started');
    } else {
        toast.error('Something has gone wrong');
    }
  }

  return (
    <BackgroundPage 
      tasks={tasks} 
      datasetTaskOptions={datasetTaskOptions} generalTaskOptions={generalTaskOptions} datasets={datasets} 
      selectedDataset={selectedDataset} selectedDatasetTask={selectedDatasetTask} selectedGeneralTask={selectedGeneralTask}
      onSelectDatasetTask={onSelectDatasetTask} onSelectGeneralTask={onSelectDatasetTask} onSelectDataset={onSelectDataset} 
      onSubmitDatasetTask={onSubmitDatasetTask} onSubmitGeneralTask={onSubmitGeneralTask}
    />
  );
}

export { BackgroundPageContainer };