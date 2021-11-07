import { toast } from 'react-toastify'
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ComponentAnnotation from '../components/ComponentAnnotation';
import Api from '../api';


function ComponentAnnotationContainer( props ) {

  const { ic_id } = useParams();
  const [ annotation, setAnnotation ] = useState({
    flag_brain: false,
    flag_mu: false,
    flag_alpha: false,
    flag_eyes: false,
    flag_eyes_blinks: false,
    flag_eyes_h: false,
    flag_eyes_v: false,
    flag_muscles_and_movement: false,
    flag_muscles: false,
    flag_movement: false,
    flag_heart: false,
    flag_noise: false,
    flag_line_noise: false,
    flag_ch_noise: false,
    flag_uncertain: false,
    flag_other: false,
    comment: ''
  });

  const [ loading, setLoading ] = useState(true);
  const [ ic, setIc ] = useState({});
  const [ dataset, setDataset ] = useState({});
  const [ subject, setSubject ] = useState({});

  useEffect(async () => {
    setLoading(true);
    let _ic = await Api.getJson(`view/ic/${ic_id}`);
    if (_ic.id) {
      setIc(_ic);
      let _subject = await Api.getJson(`view/subjects/${_ic.subject.id}`);
      setSubject(_subject);
      let _dataset = await Api.getJson(`view/datasets/${_ic.dataset}`);
      setDataset(_dataset);
    }

    let _annotation = await Api.getJson(`data/user-annotation-by-ic/${ic_id}`);
    if (_annotation.id) {
      setAnnotation(_annotation);
    }
    setLoading(false);
  }, [ic_id]);

  function handleInputChange (e) {
    const {name, checked} = e.target;
    setAnnotation({...annotation, [name]: checked});
  }

  function handleCheck (obj) {
    console.log(obj);
    setAnnotation({...annotation, ...obj});
  }

  function handleCommentFieldChange (e) {
    setAnnotation({...annotation, ['comment']: e.target.value});
  }

  async function submit () {
    let response;
    response = await Api.post(`data/user-annotation-by-ic/${ic_id}`, annotation);
    if (response.ok) {
      setAnnotation(await response.json());
      toast.success('Сохранено')
    }
  }

  return (
    <ComponentAnnotation 
      ic={ic} dataset={dataset} subject={subject} onChange={handleInputChange} handleCheck={handleCheck}
      onCommentFieldChange={handleCommentFieldChange} annotation={annotation} onSubmit={submit} loading={loading}/>    
  )
}

export default ComponentAnnotationContainer;