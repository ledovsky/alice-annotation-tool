import Breadcrumbs from '../common/Breadcrumbs';
import Link from '../common/Link';
import Spinner from '../common/Spinner';


function DatasetView (props) {
  const rows = props.subjects.map((subject) =>
    <tr key={subject.id.toString()}>
      <td className="border px-4 py-2"><a className="text-indigo-500" href={`/subjects/${subject.id}`}>{subject.name}</a></td>
    </tr>
  );
  return (
    <div className="ml-6">
      <Breadcrumbs dataset={props.dataset} />
      <div className="mt-6 ml-6" hidden={!props.loading}>
        <Spinner/>
      </div>
      <table className="table-auto mt-6" hidden={props.loading}>
        <thead>
          <tr>
            <th className="px-4 py-2">Subject</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
  )
}

export default DatasetView;