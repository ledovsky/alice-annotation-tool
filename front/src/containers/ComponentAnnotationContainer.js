import { toast } from 'react-toastify'
import { useSelector } from 'react-redux'
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ComponentAnnotation from '../components/ComponentAnnotation';
import Api from '../api';


function ComponentAnnotationContainer( props ) {

  const default_annotation = {
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
  }

  const { ic_id } = useParams();
  const [ annotation, setAnnotation ] = useState({default_annotation});
  const [ loading, setLoading ] = useState(true);
  const [ ic, setIc ] = useState({});
  const [ dataset, setDataset ] = useState({});
  const [ subject, setSubject ] = useState({});
  const [ componentsPlotObj, setComponentsPlotObj ] = useState({});
  const auth = useSelector(state => state.auth);
  let loggedIn = false;
  if (auth.token) {
    loggedIn = true;
  }

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      let _ic = await Api.getJson(`view/ic/${ic_id}`);
      if (_ic.id) {
        setIc(_ic);
        let _subject = await Api.getJson(`view/subjects/${_ic.subject.id}`);
        setSubject(_subject);
        let _dataset = await Api.getJson(`view/datasets/${_ic.dataset}`);
        setDataset(_dataset);
      }

      if (loggedIn) {
        let _annotation = await Api.getJson(`data/user-annotation-by-ic/${ic_id}`);
        if (_annotation.id) {
          setAnnotation(_annotation);
        } else {
          setAnnotation(default_annotation);
        }
      }
      setLoading(false);
    }
    fetchData();
  }, [ic_id, loggedIn]);

  // load components plot
  useEffect(() => {
    async function fetchData() {
      if (subject.id) {
        let response = await Api.getJson(`view/subjects/components-plot/${subject.id}`);
        if (response.subject_id) {
          setComponentsPlotObj(response.figure);
        }
      }
    }
    fetchData();
  }, [subject]);

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
      onCommentFieldChange={handleCommentFieldChange} annotation={annotation} onSubmit={submit} 
      loggedIn={loggedIn} componentsPlotObj={componentsPlotObj} loading={loading}/>    
  )
}

export default ComponentAnnotationContainer;