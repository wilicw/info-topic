import axios from 'axios';
import jwt_decode from "jwt-decode";
import { config } from '../config'
import vue_conf from "@/../vue.config.js"

const client = axios.create({
  baseURL: config.api,
  timeout: 100000
}
)

console.log(config.api)

export default {
  upload_image: async function (formData) {
    const _token = this.get_token();
    return client.post("/upload?type=image", formData, {
      headers: {
        "Authorization": _token,
        "Content-Type": 'multipart/form-data'
      }
    });
  },
  upload_file: async function (formData) {
    const _token = this.get_token();
    return client.post("/upload?type=file", formData, {
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
      await client.get("/auth", {
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
    client.get("/projects?highlight")
  ,
  get_random: async () =>
    client.get("/projects?random")
  ,
  get_token: () =>
    window.localStorage.getItem("token")
  ,
  clear_token: () =>
    window.localStorage.removeItem("token")
  ,
  get_topics_by_tid: async (id) =>
    client.get(`/teachers/${id}`)
  ,
  get_topics_by_year: async (y) =>
    client.get(`/projects?year=${y}`)
  ,
  get_topics_by_keyword: async (word) =>
    client.get(`/projects?keyword=${word}`)
  ,
  get_topics_search: async (word) =>
    client.get(`/projects?search=${word}`)
  ,
  get_teachers: async () =>
    client.get("/teachers")
  ,
  get_topic: async (id) =>
    client.get(`/projects/${id}`)
  ,
  get_topics_by_classification: async (year, cid) =>
    client.get(`/ranking?year=${year}&sort=${cid}`)
  ,
  get_topic_by_token: async function () {
    const _token = this.get_token();
    return client.get(`/projects?token=${_token}`)
  },
  get_score_weight: async function () {
    const _token = this.get_token();
    return client.get("/scores/weight", {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_students_by_topic: async function (uuid) {
    const _token = this.get_token();
    return client.get(`/projects/${uuid}/students`, {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_students_by_year: async function (y) {
    const _token = this.get_token();
    return client.get(`/students/year?=${y}`, {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_all_year: async () =>
    client.get(`/years`)
  ,
  set_score_weight: async function (changed_data) {
    const _token = this.get_token();
    return client.put("/scores/weight", { data: changed_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  get_score_classification: async () =>
    client.get("/scores/classification")
  ,
  create_score_classification: async function (description, global) {
    const _token = this.get_token();
    return client.post("/scores/classification", { description: description, global: global }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  update_score_classification: async function (id, description, global) {
    const _token = this.get_token();
    return client.put("/scores/classification", { id: id, description: description, global: global }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  delete_score_classification: async function (id) {
    const _token = this.get_token();
    return client.delete("/scores/classification", {
      headers: {
        Authorization: _token,
      },
      data: { id: id },
    })
  },
  set_score: async function (changed_data) {
    const _token = this.get_token();
    return client.post("/scores", { data: changed_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  set_topic: async function (uuid, topic_data) {
    const _token = this.get_token();
    return client.put(`/projects/${uuid}`, { data: topic_data }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  new_topic: async function (topic_data) {
    const _token = this.get_token();
    return client.post(`/projects`, { data: topic_data }, {
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
    return client.post(`/import_scores`, { id: classification_id, group_data: group, score_data: score }, {
      headers: {
        Authorization: _token,
      }
    })
  },
  import_student: async function (year, selected_class, name, seat_num, school_id) {
    const _token = this.get_token();
    return client.post(`/students`, { year: year, selected_class: selected_class, name: name, seat_num: seat_num, school_id: school_id }, {
      headers: {
        Authorization: _token,
      }
    })
  },
}
