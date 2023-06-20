function Datasets (props) {
  const rows = props.datasets.map((dataset) =>
    <tr key={dataset.id.toString()}>
      <td className="border px-4 py-2"><a className="text-indigo-500" href={`/datasets/${dataset.id}`}>{dataset.full_name}</a></td>
      <td className="border px-4 py-2">{dataset.stats ? dataset.stats.n_components : null}</td>
      <td className="border px-4 py-2">{dataset.stats ? dataset.stats.n_annotations : null}</td>
      <td className="border px-4 py-2">{dataset.stats ? dataset.stats.n_components_with_annotations : null}</td>
      <td className="border px-4 py-2">{dataset.stats ? dataset.stats.n_components_with_images : null}</td>
      <td className="border px-4 py-2">{dataset.stats ? dataset.stats.n_users : null}</td>
    </tr>
  );
  return (
    <div className="ml-6">
      <p className="text-4xl">Datasets</p>
      <table className="table-auto">
        <thead>
          <tr>
            <th className="px-4 py-2">Dataset</th>
            <th className="px-4 py-2">N ICs</th>
            <th className="px-4 py-2">N an-s</th>
            <th className="px-4 py-2">N ICs with an-s</th>
            <th className="px-4 py-2">N ICs with images</th>
            <th className="px-4 py-2">N annotators</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
  )
}

export default Datasets