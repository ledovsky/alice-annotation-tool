import React, { useState } from 'react';
import { useHistory } from "react-router-dom";
import {useLocation} from "react-router-dom";
import { toast } from 'react-toastify';

import Api from '../../api';
import { ResetPassword } from '../../components/auth/ResetPassword';


function ResetPasswordContainer (props) {

  let history = useHistory();
  let location = useLocation();
  const [ formData, setFormData ] = useState({password: '', password2: '', passwordsMismatch: false});

  function onChange(e) {
      let newFormData = {...formData, [e.target.name]: e.target.value};
      newFormData.passwordsMismatch = newFormData.password === newFormData.password2;
      setFormData(newFormData);
  }

  async function onSubmit() {
    const token = new URLSearchParams(location.search).get('token');
    if (!token) {
        toast.error('Error. No token for password reset');
        return;
    }
    const response = await Api.post(`password_reset/confirm/`, {password: formData.password, token: token});
    if (response.status === 200) {
      toast.success('Password was successfully reset')
      history.push('/login')
    }
  }

  return (
    <ResetPassword onChange={onChange} onSubmit={onSubmit} formData={formData}/>
  )
}

export { ResetPasswordContainer };