import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useSelector } from 'react-redux';

import Api from '../api'
import SubjectView from '../components/SubjectView'


function DatasetViewContainer(props) {

  const { subject_id } = useParams();


  const [ loading, setLoading ] = useState(true);
  const [ params, setParams ] = useState({});
  const [ subject, setSubject ] = useState({});
  const [ dataset, setDataset ] = useState({});
  const [ ics, setIcs ] = useState([]);

  useEffect(async () => {
    setLoading(true);
    let subject = await Api.getJson(`view/subjects/${subject_id}`);
    setSubject(subject);
    if (subject.id) {
        let dataset = await Api.getJson(`view/datasets/${subject.dataset}`);
        setDataset(dataset);
        let collection = await Api.getList(`view/ic/list/by-subject/${subject.id}`);
        setIcs(collection);
    }
    setLoading(false);
  }, [ params ]);

  return (
    <SubjectView dataset={dataset} subject={subject} ics={ics} loading={loading} />
  )
}

export default DatasetViewContainer