import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { BackgroundPage } from "../components/BackgroundPage";
import Api from '../api';


function BackgroundPageContainer (props) {

  const taskOptions = [
    {
        name: 'Update plots',
        value: 'update-ic-plots'
    },
    {
        name: 'Update links',
        value: 'update-links'
    },
  ]
  const [ datasets, setDatasets ] = useState([]);
  const [ selectedTask, setSelectedTask ] = useState(taskOptions[0].value);
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

  async function onSelectTask(e) {
    setSelectedTask(e.target.value);
  }

  async function onSubmit() {
    let response = await Api.post(`background/run-dataset`, {dataset_id: selectedDataset, task_name: selectedTask});
    let data = await response.json();
    if (data.status == 'ok') {
        toast.success('Task successfully started');
    } else {
        toast.error('Something has gone wrong');
    }
  }

  return (
    <BackgroundPage taskOptions={taskOptions} datasets={datasets} 
    selectedDataset={selectedDataset} selectedTask={selectedTask}
    tasks={tasks} onSelectTask={onSelectTask} onSelectDataset={onSelectDataset} onSubmit={onSubmit}/>
  );
}

export { BackgroundPageContainer };