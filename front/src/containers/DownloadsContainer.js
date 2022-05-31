import React, { useState, useEffect } from 'react';
import Api from '../api';
import Downloads from '../components/Downloads';


function DownloadsContainer (props) {
  const [ actual, setActual ] = useState([]);

  useEffect(async () => {
    let _actual = await Api.getList(`downloads/actual`);
    setActual(_actual);
  }, []);
  return <Downloads actual={actual}/>
}

export default DownloadsContainer;