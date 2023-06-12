import { toast } from 'react-toastify'
import { isEmpty } from 'lodash'
import store from './store';


const queryString = require('query-string')

class Api {
  url = process.env.REACT_APP_API_URL + "/";

  async getList(path, params) {
    let response = await this.get(path, params)
    if (response.ok) {
      return response.json()
    } else {
      return []
    }
  }

  async getJson(path, params) {
    let response = await this.get(path, params)
    if (response.ok) {
      return response.json()
    } else {
      return {}
    }
  }

  async get (path, params) {
    path = this.url + path
    path = isEmpty(params) ? path : (path + '?' + queryString.stringify(params))
    let response = await fetch(path, {
      headers: this.getHeaders()
    })
    return this.handleErrors(response)
  }

  async post (path, data) {
    return this.postLike(path, data, 'POST')
  }

  async put (path, data) {
    return this.postLike(path, data, 'PUT')
  }

  async patch (path, data) {
    return this.postLike(path, data, 'PATCH')
  }

  async postLike (path, data, method) {
    path = this.url + path
    let response = await fetch(path, {
      method: method,
      headers: this.getHeaders(),
      body: JSON.stringify(data)
    })
    return this.handleErrors(response, {});
  }

  async handleErrors(response) {
    if (!response.ok) {
      toast.error("Error in " + response.url + "; Status " + response.status.toString())
    }
    return response
  }

  getHeaders() {
    let headers = {
      'Content-Type': 'application/json'
    }
    const auth = store.getState()['auth']
    if (auth.token) {
      headers["Authorization"] = `Token ${ auth.token }`
    }
    return headers;

  }

}

export default new Api()