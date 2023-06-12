import Link from '../common/Link';

function Breadcrumbs (props) {
  return (
    <p>
        <Link href="/datasets">Datasets</Link>
        {
            props.dataset ?
            <> <span> / </span> <Link href={`/datasets/${props.dataset.id}`}>{props.dataset.full_name}</Link> </>
            : ''
        }
        {
            props.subject ?
            <> <span> / </span> <Link href={`/subjects/${props.subject.id}`}>{props.subject.name}</Link> </>
            : ''
        }
        {
            props.ic ?
            <> <span> / </span> <Link href={`/ic/${props.ic.id}/annotate`}>{props.ic.name}</Link> </>
            : ''
        }
    </p>
  )
}
        
export default Breadcrumbs;