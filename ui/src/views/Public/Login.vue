<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="4">
        <v-card
          :flat="$vuetify.breakpoint.mobile"
          class="pa-5"
          :class="{ transparent: $vuetify.breakpoint.mobile }"
        >
          <v-form @submit.prevent="login">
            <v-card-title class="font-weight-bold">登入</v-card-title>
            <v-card-text>
              <p class="text--secondary">
                帳號請輸入 畢業級別+班級+座號
                ，例如108年畢業甲班55號，請輸入108a55
              </p>
              <v-text-field
                v-model="account"
                label="帳號"
                required
                :rules="rules"
                class="mt-8"
              ></v-text-field>
              <v-text-field
                v-model="pass"
                label="密碼"
                required
                type="password"
                :rules="rules"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" type="submit">送出</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "Login",
  data: () => ({
    pass: "",
    account: "",
    rules: [(value) => !!value || "此欄位不可空白！"],
  }),
  async created() {
    document.title = `登入 || ${config.title}`;
    if (await api.is_login()) this.$router.push("/menu");
  },
  methods: {
    async login() {
      const username = this.account,
        password = this.pass;
      try {
        const res = await api.login(username, password);
        api.storage_token(res.data);
        this.$store.commit("login");
        this.$router.push("/menu");
      } catch {
        this.$store.commit("show_popup", { s: "err", msg: "帳號或密碼錯誤" });
      }
    },
  },
};
</script>
