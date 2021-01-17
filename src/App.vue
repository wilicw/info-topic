<template>
  <v-app>
    <v-app-bar app flat class="mt-5 mx-3" color="white" absolute>
      <div class="d-flex align-center" @click="$router.push('/')">
        <v-img
          alt="Logo"
          class="shrink mr-3"
          contain
          src="/logo.svg"
          transition="scale-transition"
          width="30"
        />
        <p class="headline mt-3">
          <span class="font-weight-bold" v-if="!$vuetify.breakpoint.mobile"
            >大安資訊
          </span>
          <span>專題網</span>
        </p>
      </div>

      <v-spacer></v-spacer>

      <div v-if="!$vuetify.breakpoint.mobile">
        <v-btn
          v-for="link in nav_link"
          :key="link.url"
          @click="$router.push(link.url)"
          text
        >
          <span class="subtitle-1 font-weight-medium">{{ link.text }}</span>
        </v-btn>
      </div>

      <v-app-bar-nav-icon
        v-if="$vuetify.breakpoint.mobile"
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
            @click="
              drawer = false;
              $router.push(link.url);
            "
          >
            <v-list-item-title>{{ link.text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    drawer: false,
    nav_link: [
      {
        text: "首頁",
        url: "/",
      },
      {
        text: "搜尋專題",
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
        text: "登入",
        url: "/login",
      },
    ],
  }),
};
</script>