import Breadcrumbs from '../common/Breadcrumbs';
import Link from '../common/Link';

function AnnotationBar (props) {
  return (
    <div className="mx-6 flex">
      <Breadcrumbs dataset={props.dataset} subject={props.subject} ic={props.ic} />
      {/* { props.state == 'annotation' ?
        <p className="ml-6"><Link href={`/ic/${props.ic.id}`}>Annotations</Link></p> : ''
      } */}
      { props.state == 'list' ?
        <p className="ml-6"><Link href={`/ic/${props.ic.id}/annotate`}>Annotate</Link></p> : ''
      }
      { props.ic.links && props.ic.links.prev ?
        <p className="ml-6">
          <Link href={`/ic/${props.ic.links.prev}${ props.state == 'annotation' ? '/annotate' : ''}`}>Previous</Link></p> :
        ''
      }
      { props.ic.links && props.ic.links.next ?
        <p className="ml-6">
          <Link href={`/ic/${props.ic.links.next}${ props.state == 'annotation' ? '/annotate' : ''}`}>Next</Link></p> :
        ''
      }
    </div>
  )
}

export default AnnotationBar;