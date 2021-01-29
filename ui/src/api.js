import axios from 'axios';
import { api, imgur_client_id } from '../vue.config'

const config = {
  baseURL: api,
  timeout: 100000
}

const client = axios.create(config)

export default {
  upload_image: async (formData) => {
    const res = await axios({
      method: 'POST',
      url: 'https://api.imgur.com/3/image',
      data: formData,
      headers: {
        Authorization: 'Client-ID ' + imgur_client_id,
      },
      mimeType: 'multipart/form-data',
    });
    return res.data.data;
  },
  login: async (username, password) =>
    client.post("/auth", {
      username: username,
      password: password
    })
  ,
  storage_token: (token) =>
    window.localStorage.setItem("token", String(token))
}