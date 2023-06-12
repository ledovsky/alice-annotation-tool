import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import AnnotationList from '../components/AnnotationList';
import Api from '../api';


function AnnotationListContainer (props) {

  const { ic_id } = useParams();
  const [ ic, setIc ] = useState({})
  const [ annotations, setAnnotations ] = useState([]);
  const [ dataset, setDataset ] = useState({});

  useEffect(async () => {
    let _ic = await Api.getJson(`view/ic/${ic_id}`, {})
    if (_ic.id) {
      setIc(_ic)
      let _dataset = await Api.getJson(`view/datasets/${_ic.dataset}`);
      setDataset(_dataset);
    }
    let _annotations = await Api.getList('view/annotations/list', { ic_id: ic_id })
    setAnnotations(_annotations)
  }, [ic_id]);

  return (
    <AnnotationList annotations={annotations} dataset={dataset} ic={ic}/>
  )
}

export default AnnotationListContainer;