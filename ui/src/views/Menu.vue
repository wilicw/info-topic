<template>
  <v-container>
    <v-row justify="" class="mt-5 fill-height" align="center">
      <v-col v-for="i in options.menu" :key="i.url" cols="12" sm="4">
        <v-hover v-slot="{ hover }">
          <v-card
            :elevation="hover ? 5 : 2"
            class="rounded-0 pa-10 ma-1 hover"
            @click="$router.push(i.url)"
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
    options: {
      menu: [],
      common: [
        {
          text: "編輯專題",
          url: "edit",
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
          url: "view",
          icon: "mdi-book-open-page-variant",
        },
      ],
      teacher: [
        {
          text: "評分",
          url: "score",
          icon: "mdi-check-all",
        },
        {
          text: "編輯學生",
          url: "edit_stu",
          icon: "mdi-account-lock",
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
  created() {
    this.load_identity();
  },
  methods: {
    load_identity() {
      if (!api.is_login()) {
        this.$route.go("login");
        return;
      }
      const data = JSON.parse(atob(api.get_token().split(".")[1]));
      switch (data.group) {
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
