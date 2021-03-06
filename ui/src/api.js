import axios from 'axios';
import jwt_decode from "jwt-decode";
import { config } from '../config'
import vue_conf from "@/../vue.config.js"

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
  get_highlight: async () =>
    client.get("/highlight")
  ,
  get_random: async () =>
    client.get("/random")
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
  get_topics_by_classification: async (year, cid) =>
    client.get(`/get_topics_by_classification/${year}/${cid}`)
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
  get_all_year: async () =>
    client.get(`/year/`)
  ,
  set_score_weight: async function (changed_data) {
    const _token = this.get_token();
    return client.put("/score_weight", { data: changed_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_score_classification: async () =>
    client.get("/score_classification")
  ,
  create_score_classification: async function (description, global) {
    const _token = this.get_token();
    return client.post("/score_classification", { description: description, global: global }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  update_score_classification: async function (id, description, global) {
    const _token = this.get_token();
    return client.put("/score_classification", { id: id, description: description, global: global }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  delete_score_classification: async function (id) {
    const _token = this.get_token();
    return client.delete("/score_classification", {
      headers: {
        Authorization: _token,
      },
      data: { id: id },
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
  get_reference: async () =>
    axios.get(`${vue_conf.publicPath}upload/etc/reference.html`)
  ,
  import_score: async function (classification_id, group, score) {
    const _token = this.get_token();
    return client.post(`/import_score`, { id: classification_id, group_data: group, score_data: score }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  import_student: async function (name, account, school_id) {
    const _token = this.get_token();
    return client.post(`/import_student`, { name: name, account: account, school_id: school_id }, {
      headers: {
        Authorization: _token,
      }
    })
  },
}
