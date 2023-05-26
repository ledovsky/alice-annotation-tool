import React from 'react';


function AdminPage (props) {
 
  const dataset_rows = props.datasets.map((dataset, idx) =>
    <option key={dataset.id} value={dataset.id}>{dataset.full_name}</option>
  );

  const task_rows = props.tasks.map((row, idx) =>
    <tr key={idx}>
      <td className="border px-4 py-2">{row.status}</td>
      <td className="border px-4 py-2">{row.dataset}</td>
      <td className="border px-4 py-2">{row.time_start}</td>
    </tr>
  );

  return (
    <div className="ml-6">
      <p className="text-4xl mb-6">Admin page</p>
      <p className="text-2xl mb-3">Run dataset recalculation</p>
      <form>
        <div className="md:flex md:items-center mb-6">
          <select className="form-select text-sm" value={props.selectedDataset} onChange={props.onSelect}>
            {dataset_rows}
          </select>
          <button className="ml-3 bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" 
                  onClick={ e => props.onSubmit(e) }>
            Start
          </button>

        </div>
      </form>

      <p className="text-2xl mb-3">Active Tasks</p>
      <table className="table-auto">
        <thead>
          <tr>
            <th className="px-4 py-2">Status</th>
            <th className="px-4 py-2">Dataset</th>
            <th className="px-4 py-2">Time started</th>
          </tr>
        </thead>
        <tbody>
          {task_rows}
        </tbody>
      </table>

    </div>

  )
}

export { AdminPage };