import React from 'react';
import Moment from 'moment';


function BackgroundPage (props) {
 
  const datasetRows = props.datasets.map((dataset, idx) =>
    <option key={dataset.id} value={dataset.id}>{dataset.full_name}</option>
  );

  const taskOptionRows = props.taskOptions.map(option =>
    <option key={option.value} value={option.value}>{option.name}</option>
  );

  const task_rows = props.tasks.map((row, idx) =>
    <tr key={idx}>
      <td className="border px-4 py-2">{row.task}</td>
      <td className="border px-4 py-2">{Moment(row.created).format('YYYY-MM-D hh:mm:ss')}</td>
      <td className="border px-4 py-2">{Moment(row.updated).format('YYYY-MM-D hh:mm:ss')}</td>
      <td className="border px-4 py-2">{row.status}</td>
      <td className="border px-4 py-2">{row.details}</td>
    </tr>
  );

  return (
    <div className="ml-6">
      <p className="text-4xl mb-6">Admin page</p>
      <p className="text-2xl mb-3">Run background task</p>
      <form>
        <div className="md:flex md:items-center mb-6">
          <select className="form-select text-sm" value={props.selectedDataset} onChange={props.onSelectDataset}>
            {datasetRows}
          </select>
          <select className="ml-3 form-select text-sm" value={props.selectedTask} onChange={props.onSelectTask}>
            {taskOptionRows}
          </select>
          <button className="ml-3 bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" 
                  onClick={ e => props.onSubmit(e) }>
            Start
          </button>

        </div>
      </form>

      <p className="text-2xl mb-3">Last tasks</p>
      <table className="table-auto">
        <thead>
          <tr>
            <th className="px-4 py-2">Task</th>
            <th className="px-4 py-2">Created</th>
            <th className="px-4 py-2">Updated</th>
            <th className="px-4 py-2">Status</th>
            <th className="px-4 py-2">Details</th>
          </tr>
        </thead>
        <tbody>
          {task_rows}
        </tbody>
      </table>

    </div>

  )
}

export { BackgroundPage };