import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

import { Login } from '../../components/auth/Login';
import { login } from '../../actions/authActions'



function LoginContainer (props) {

  let history = useHistory();
  const [ formData, setFormData ] = useState({username: '', password: ''});
  const [ wrongCredentials, setWrongCredentials ] = useState(false);

  function onChange(e) {
      let newFormData = {...formData, [e.target.name]: e.target.value};
      setFormData(newFormData);
  }

  async function onSubmit() {
    login(formData.username, formData.password)
      .then(response => {
        if (response.ok) {
          history.push('/')
        } else {
          setWrongCredentials(true)
        }
      })
  }

  return (
    <Login wrongCredentials={wrongCredentials} onChange={onChange} onSubmit={onSubmit}/>
  )
}

export { LoginContainer };