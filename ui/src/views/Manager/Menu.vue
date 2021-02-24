<template>
  <v-container>
    <v-row class="mt-5 fill-height" align="center">
      <v-col v-for="i in options.menu" :key="i.url" cols="12" sm="4">
        <v-hover v-slot="{ hover }">
          <v-card
            :elevation="hover ? 5 : 2"
            class="rounded-0 pa-10 ma-1 hover"
            @click="i.url && $router.push(i.url)"
            :disabled="i.url == null"
          >
            <v-card-title class="headline font-weight-bold">
              <v-icon large class="mr-5 mt-1">{{ i.icon }}</v-icon> {{ i.text }}
            </v-card-title>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from "@/api";

export default {
  name: "Menu",
  data: () => ({
    first_login: true,
    options: {
      menu: [],
      common: [
        {
          text: "編輯專題",
          url: null,
          icon: "mdi-pen",
        },

        {
          text: "修改密碼",
          url: "change_password",
          icon: "mdi-lock-open-outline",
        },
        {
          text: "登出",
          url: "logout",
          icon: "mdi-exit-run",
        },
      ],
      stu: [
        {
          text: "檢視專題",
          url: null,
          icon: "mdi-book-open-page-variant",
        },
      ],
      teacher: [
        {
          text: "評分",
          url: "score",
          icon: "mdi-check-all",
        },
      ],
      admin: [
        {
          text: "修改分數權重",
          url: "change_weight",
          icon: "mdi-math-integral-box",
        },
        {
          text: "編輯帳號",
          url: "edit_account",
          icon: "mdi-account-lock",
        },
      ],
    },
  }),
  async created() {
    this.load_identity();
    document.title = `個人頁面 || 大安資訊專題網`;
    try {
      const res = await api.get_topic_by_token();
      let id = res.data.id;
      if (id == undefined) {
        this.options.common[0].url = "edit_topics";
      } else if (id == -1) {
        this.options.stu[0].url = "new";
        this.options.stu[0].text = "建立專題";
        this.options.stu[0].icon = "mdi-plus";
      } else {
        this.options.stu[0].url = `topic/${id}`;
        this.options.common[0].url = `edit/${id}`;
      }
    } catch {
      this.options.common[0].url = "edit_topics";
    }
  },
  methods: {
    async load_identity() {
      if (!(await api.is_login())) {
        this.$router.push("logout");
        return;
      }
      switch (api.get_group()) {
        case "stu":
          this.options.menu = this.options.stu.concat(this.options.common);
          break;
        case "teacher":
          this.options.menu = this.options.teacher.concat(this.options.common);
          break;
        case "admin":
          this.options.menu = this.options.admin.concat(this.options.common);
          break;
        default:
          this.$route.go("login");
          break;
      }
    },
  },
};
</script>
