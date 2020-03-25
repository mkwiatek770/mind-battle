import axios from 'axios'
import Cookies from 'js-cookie'

export const HTTP = axios.create({
  baseURL: 'http://0.0.0.0:8000/api/v1/',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken')
  }
})
