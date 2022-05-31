import React, { useState, useEffect } from 'react';

import Api from '../api';
import Dataset from '../components/Datasets';


function Datasets(props) {

  const [ datasets, setDatasets ] = useState([]);

  useEffect(async () => {
    // Update the document title using the browser API      
    let collection = await Api.getList('view/datasets/list', {})
    setDatasets(collection)
  }, []);


  return (
    <Dataset datasets={datasets} />
  )
}

export default Datasets