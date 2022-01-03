import { toast } from 'react-toastify';
import store from '../store';
import api from '../api';


export async function login(login, password){
  let response = await api.post("auth", { username: login, password: password })
  if (response.ok) {
    let data = await response.json()
    localStorage.setItem("auth", JSON.stringify(data))
    store.dispatch({
      type: "AUTH_LOG_IN",
      payload: data
    })
    toast.success(`Welcome, ${ data.user.first_name }`)
  }
  return response
}

export function logout(){
  localStorage.removeItem("auth")
  store.dispatch({
    type: "AUTH_LOG_OUT"
  })
}
