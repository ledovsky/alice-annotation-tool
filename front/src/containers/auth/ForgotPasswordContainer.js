import React, { useState } from 'react';
import { useHistory } from "react-router-dom";
import { toast } from 'react-toastify';

import Api from '../../api';
import { ForgotPassword } from '../../components/auth/ForgotPassword';


function ForgotPasswordContainer (props) {

  let history = useHistory();
  const [ formData, setFormData ] = useState({email: ''});

  function onChange(e) {
      let newFormData = {...formData, [e.target.name]: e.target.value};
      setFormData(newFormData);
  }

  async function onSubmit() {
    const response = await Api.post(`password_reset/`, {email: formData.email});
    if (response.status === 400) {
      const responseJson = await response.json();
      toast.error(responseJson.email[0]);
      return;
    }  
    if (response.status === 200) {
      toast.success('Email with a password reset link was sent. Please, check your mailbox');
      history.push('/');
    }
  }
  return (
    <ForgotPassword onChange={onChange} onSubmit={onSubmit} formData={formData}/>
  )
}

export { ForgotPasswordContainer };