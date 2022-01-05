import Breadcrumbs from '../common/Breadcrumbs';
import { Link } from 'react-router-dom';

import Spinner from '../common/Spinner';
import { annotationClasses } from '../Constants';


function SubjectView (props) {
  const ics = props.ics.map((ic) => {
    let tags = Object.entries(ic.annotation).map(([key, value]) => {
      if (key.includes("flag") && value === true) {
        return annotationClasses[key].name;
      } else {
        return null;
      }
    });
    tags = tags.filter(tag => tag !== null);
    tags = tags.map(tag => {
      return (
        <span class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-indigo-100 bg-indigo-600 rounded mr-2 mt-2">{tag}</span>
      )
    })
    return (
      <div className="w-full max-w-xs px-6 py-6" key={ic.id}>
        <Link to={`/ic/${ic.id}/annotate`}>
          <p className="text-center font-bold">{ic.name}</p>
          { ic.images ?
            <img src={ic.images.img_topomap} alt=""/> : <div></div>
          }
        </Link>
        <div className="w-full text-center content-center">
          { tags.length ?
            <div class="flex flex-wrap">{tags}</div>  :
            <p>Is not annotated</p>
          }
        </div>
      </div>
  )}
  );
  return (
    <div className="ml-6">
      <Breadcrumbs dataset={props.dataset} subject={props.subject} />
      <div className="mt-6 ml-6" hidden={!props.loading}>
        <Spinner/>
      </div>
      <div className="flex flex-wrap">
        {ics}
      </div>
    </div>
  )
}

export default SubjectView;