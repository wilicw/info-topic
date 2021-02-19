import axios from 'axios';
import { config } from '../config'

const client = axios.create({
  baseURL: config.api,
  timeout: 100000
}
)

export default {
  upload_image: async (formData) => {
    const res = await axios({
      method: 'POST',
      url: 'https://api.imgur.com/3/image',
      data: formData,
      headers: {
        Authorization: 'Client-ID ' + config.imgur_client_id,
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
  storage_token: (token) => {
    console.log(token);
    window.localStorage.setItem("token", token);
  }
  ,
  is_login: async function () {
    if (window.localStorage.getItem("token") == null || window.localStorage.getItem("token") == undefined || window.localStorage.getItem("token") == "") return false
    const _token = this.get_token();
    try {
      client.post("/is_login", {}, {
        headers: {
          Authorization: _token,
        }
      })
      return true
    } catch {
      return false
    }
  }
  ,
  get_token: () =>
    window.localStorage.getItem("token")
  ,
  clear_token: () =>
    window.localStorage.removeItem("token")
  ,
  get_topics_by_tid: async (id) =>
    client.get(`/teacher/${id}`)
  ,
  get_topics_by_keyword: async (word) =>
    client.get(`/keyword/${word}`)
  ,
  get_topics_search: async (word) =>
    client.get(`/search/${word}`)
  ,
  get_teachers: async () =>
    client.get("/teacher/")
  ,
  get_topic: async (id) =>
    client.get(`/topic/${id}`)
  ,
  download: (id) =>
    window.open(`${config.api}/file/${id}`, '_blank')
  ,
  change_password: async function (original_pass, pass) {
    const _token = this.get_token();
    return client.post("/change_password", {
      original_pass: original_pass,
      pass: pass
    }, {
      headers: {
        Authorization: _token,
      }
    })
  }
  ,
}