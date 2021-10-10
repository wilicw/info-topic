<template>
  <v-app style="overflow-x: hidden">
    <v-app-bar
      app
      flat
      class="mt-5 noselect"
      :class="{ 'mx-5': !$vuetify.breakpoint.mobile }"
      style="background-color: transparent"
      absolute
    >
      <div class="d-flex align-center" @click="$router.push('/')">
        <v-img
          alt="Logo"
          class="shrink mr-3"
          contain
          :src="$vuetify.theme.dark ? logo_dark : logo"
          transition="scale-transition"
          width="25"
        ></v-img>
        <p class="headline mt-3 hover">
          <span class="font-weight-bold" v-if="!$vuetify.breakpoint.mobile"
            >大安資訊
          </span>
          <span>專題網</span>
        </p>
      </div>

      <v-spacer></v-spacer>

      <div v-if="!$vuetify.breakpoint.mobile">
        <span
          @click="
            $router.push(link.url).catch((err) => {
              err;
            })
          "
          v-for="link in nav_link"
          :key="link.url"
          class="subtitle-1 font-weight-medium mx-5 hover"
        >
          {{ link.text }}
        </span>
      </div>

      <v-btn @click="toggle_theme" icon class="px-2">
        <v-icon>mdi-theme-light-dark</v-icon>
      </v-btn>

      <v-app-bar-nav-icon
        v-if="$vuetify.breakpoint.mobile"
        class="mx-1"
        @click.stop="drawer = !drawer"
      ></v-app-bar-nav-icon>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      right
      absolute
      temporary
      v-if="$vuetify.breakpoint.mobile && drawer"
    >
      <v-list dense>
        <v-list-item v-for="link in nav_link" :key="link.url" link>
          <v-list-item-content
            class="mt-1"
            @click="
              drawer = false;
              $router.push(link.url).catch((err) => {
                err;
              });
            "
          >
            <v-list-item-title class="py-1">{{ link.text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
    <Footer />
    <Popup />
  </v-app>
</template>

<script>
import Footer from "@/components/Footer.vue";
import Popup from "@/components/Popup.vue";
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "App",
  components: {
    Footer,
    Popup,
  },
  data: () => ({
    drawer: false,
    logo: "",
    nav_link: [
      {
        text: "首頁",
        url: "/",
      },
      {
        text: "瀏覽",
        url: "/year/latest",
      },
      {
        text: "排名",
        url: "/rank/latest",
      },
      {
        text: "搜尋",
        url: "/search",
      },
      {
        text: "指導老師",
        url: "/teachers",
      },
      {
        text: "參考資料",
        url: "/reference",
      },
      {
        text: "",
        url: "",
      },
    ],
  }),
  computed: {
    is_login: function () {
      return this.$store.state.is_login;
    },
  },
  watch: {
    is_login: function (value) {
      if (value) {
        this.login();
      } else {
        this.logout();
      }
    },
  },
  async created() {
    this.$vuetify.theme.dark = window.localStorage.getItem("dark") != "false";
    this.logo = config.logo;
    this.logo_dark = config.logo_dark;
    if (await api.is_login()) {
      this.$store.commit("login");
      this.login();
    } else {
      this.$store.commit("logout");
      this.logout();
    }
  },
  methods: {
    logout() {
      api.clear_token();
      this.nav_link[6].text = "登入";
      this.nav_link[6].url = "/login";
    },
    login() {
      this.nav_link[6].text = "個人頁面";
      this.nav_link[6].url = "/menu";
    },
    toggle_theme() {
      window.localStorage.setItem("dark", !this.$vuetify.theme.dark);
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },
  },
};
</script>

<style>
.transparent {
  background-color: transparent;
}
.hover:hover {
  cursor: pointer;
  transition-duration: 0.3s;
}
.content {
  line-height: 2em;
  white-space: pre-line;
}

*::selection {
  background: rgba(104, 198, 130, 0.5);
}
.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Edge, Opera and Firefox */
}
</style>
<style lang="scss">
@import "@/styles/variables.scss";
</style>
