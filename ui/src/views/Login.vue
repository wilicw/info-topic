<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="4">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-card-title class="font-weight-bold">登入</v-card-title>
          <v-alert
            :value="err"
            color="pink"
            dark
            border="top"
            icon="mdi-close"
            transition="scale-transition"
          >
            帳號或密碼錯誤
          </v-alert>
          <v-card-text>
            帳號請輸入 畢業級別+班級+座號 ，例如108年畢業甲班55號，請輸入108a55
            <br />
            <br />
            <v-text-field
              v-model="account"
              label="帳號"
              required
            ></v-text-field>
            <v-text-field v-model="pass" label="密碼" required></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="login">送出</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from "@/api";

export default {
  name: "Login",
  data: () => ({
    pass: "",
    account: "",
    err: null,
  }),
  methods: {
    async login() {
      const username = this.account,
        password = this.pass;
      let res;
      try {
        res = await api.login(username, password);
      } catch {
        this.err = true;
      }
      api.storage_token(res.data);
      this.err = null;
      this.$root.$emit("login");
      this.$router.push("/menu");
    },
  },
};
</script>
