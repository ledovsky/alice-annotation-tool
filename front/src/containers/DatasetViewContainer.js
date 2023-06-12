import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useSelector } from 'react-redux';

import Api from '../api'
import DatasetView from '../components/DatasetView'


function DatasetViewContainer(props) {

  const { dataset_id } = useParams();


  const [ loading, setLoading ] = useState(true);
  const [ params, setParams ] = useState({});
  const [ dataset, setDataset ] = useState({});
  const [ subjects, setSubjects ] = useState([]);

  const datasets = useSelector(state => state.datasets);
  console.log(datasets);

  useEffect(async () => {
    setLoading(true);
    let dataset = await Api.getJson(`view/datasets/${dataset_id}`);
    setDataset(dataset);
    let collection = await Api.getList(`view/subjects/list/by-dataset/${dataset_id}`);
    setSubjects(collection);
    setLoading(false);
  }, [ params ]);


  return (
    <DatasetView dataset={dataset} subjects={subjects} loading={loading} />
  )
}

export default DatasetViewContainer