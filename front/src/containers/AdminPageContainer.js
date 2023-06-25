import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { AdminPage } from "../components/AdminPage";
import Api from '../api';


function AdminPageContainer (props) {

  const [ datasets, setDatasets ] = useState([]);
  const [ selectedDataset, setSelectedDataset ] = useState(-1);
  const [ tasks, setTasks ] = useState([]);

  async function updateTasks() {
    let collection = await Api.getJson('view/celery-list', {});
    let rows_active = Object.entries(collection.active).flatMap(([worker, tasks]) => {
      return tasks.map(task => {
        return {status: 'Active', dataset: task.args[0], time_start: new Date(task.time_start * 1000).toISOString()}
      })
    });
    let rows_reserved = Object.entries(collection.reserved).flatMap(([worker, tasks]) => {
      return tasks.map(task => {
        return {status: 'Waiting', dataset: task.args[0], time_start: ""}
      })
    });
    setTasks(rows_active.concat(rows_reserved));

  }

  useEffect(() => {
    async function fetchData() {
      let collection = await Api.getList('view/datasets/list', {});
      setDatasets(collection);
      setSelectedDataset(collection[0].id);
    }
    fetchData();
    updateTasks();
    let timer = setTimeout(
      function run() {
        updateTasks();
        timer = setTimeout(run, 5000);
      }, 5000
    )
  }, []);

  async function onSelect(e) {
    setSelectedDataset(e.target.value);
  }

  async function onSubmit() {
    Api.get(`view/recalc-dataset/${selectedDataset}`);
    toast.success('Task successfully started');
  }


  return (
    <AdminPage datasets={datasets} selectedDataset={selectedDataset} tasks={tasks} onSelect={onSelect} onSubmit={onSubmit}/>
  );
}

export { AdminPageContainer };