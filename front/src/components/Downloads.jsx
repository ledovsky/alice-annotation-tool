function Row (props) {
  return <td className="px-4 py-4">{props.children}</td>
}

function Downloads (props) {
  const rows = props.actual.map((item) => 
    <tr key={item.id}>
      <Row>{item.dataset.full_name}</Row>
      <Row>{item.dataset.description}</Row>
      <Row>{item.version}</Row>
      <Row><a className="text-indigo-500 hover:text-indigo-600" href={`${item.file}`} onClick={props.onClick}>Download</a></Row>
    </tr> 
  );

  return (
    <div className="mx-6">
      <p className="text-4xl">Downloads</p>
      <table className="table-auto mt-6">
        <thead>
          <tr>
            <th className="px-4 py-2">Dataset</th>
            <th className="px-4 py-2">Description</th>
            <th className="px-4 py-2">Version</th>
            <th className="px-4 py-2">Link</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
  );
}

export default Downloads;