import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { annotationClasses } from '../Constants';
import Api from '../api';
import SubjectView from '../components/SubjectView';


function DatasetViewContainer(props) {

  const { subject_id } = useParams();

  const [ loading, setLoading ] = useState(true);
  const [ subject, setSubject ] = useState({});
  const [ dataset, setDataset ] = useState({});
  const [ ics, setIcs ] = useState([]);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      let subject = await Api.getJson(`view/subjects/${subject_id}`);
      setSubject(subject);
      if (subject.id) {
          let dataset = await Api.getJson(`view/datasets/${subject.dataset}`);
          setDataset(dataset);
          let ics_collection = await Api.getList(`view/ic/list/by-subject/${subject.id}`);
          setIcs(ics_collection);
      }
      setLoading(false);
    }

    fetchData();
  }, [ subject_id ]);

  return (
    <SubjectView dataset={dataset} subject={subject} ics={ics} loading={loading} />
  )
}

export default DatasetViewContainer