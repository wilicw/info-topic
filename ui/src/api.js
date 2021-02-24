import axios from 'axios';
import jwt_decode from "jwt-decode";
import { config } from '../config'

const client = axios.create({
  baseURL: config.api,
  timeout: 100000
}
)

export default {
  upload_image: async function (formData) {
    const _token = this.get_token();
    return client.post("/upload_img", formData, {
      headers: {
        "Authorization": _token,
        "Content-Type": 'multipart/form-data'
      }
    });
  },
  upload_file: async function (formData) {
    const _token = this.get_token();
    return client.post("/upload", formData, {
      headers: {
        "Authorization": _token,
        "Content-Type": 'multipart/form-data'
      }
    });
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
      await client.post("/is_login", {}, {
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
  get_topics_by_year: async (y) =>
    client.get(`/year/${y}`)
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
  get_topic_by_token: async function () {
    const _token = this.get_token();
    return client.post("/get_topic_by_token", {}, {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_score_weight: async function () {
    const _token = this.get_token();
    return client.get("/score_weight", {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_students_by_topic: async function (uuid) {
    const _token = this.get_token();
    return client.get(`/get_students_by_topic/${uuid}`, {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_students_by_year: async function (y) {
    const _token = this.get_token();
    return client.get(`/get_students_by_year/${y}`, {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_score_classification: async function () {
    const _token = this.get_token();
    return client.get("/score_classification", {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_all_year: async () =>
    client.get(`/year/`)
  ,
  set_score_weight: async function (changed_data) {
    const _token = this.get_token();
    return client.post("/score_weight", { data: changed_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  set_score: async function (changed_data) {
    const _token = this.get_token();
    return client.post("/score", { data: changed_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  set_topic: async function (uuid, topic_data) {
    const _token = this.get_token();
    return client.put(`/topic/${uuid}`, { data: topic_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  new_topic: async function (topic_data) {
    const _token = this.get_token();
    return client.post(`/topic`, { data: topic_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  download: (id) =>
    window.open(`${config.api} / file / ${id}`, '_blank')
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
  lazy_load_img: (url) => {
    if (url.includes("http://") || url.includes("https://")) {
      return url;
    }
    return url.replace(/^upload/i, "upload-lazy");
  },
  get_username: function () {
    const _token = this.get_token();
    return jwt_decode(_token).username;
  },
  get_group: function () {
    const _token = this.get_token();
    return jwt_decode(_token).group;
  },
}