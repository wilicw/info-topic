<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="4">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form @submit.prevent="submit">
            <v-card-title class="font-weight-bold">修改密碼</v-card-title>
            <v-card-text>
              <v-text-field
                v-model="original_pass"
                label="原密碼"
                required
                :rules="rules"
                type="password"
              ></v-text-field>
              <v-text-field
                v-model="pass"
                label="新密碼"
                required
                type="password"
                :rules="rules"
              ></v-text-field>
              <v-text-field
                v-model="pass_rep"
                label="重複新密碼"
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
  name: "Change_password",
  data: () => ({
    original_pass: "",
    pass: "",
    pass_rep: "",
    rules: [(value) => !!value || "此欄位不可空白！"],
  }),
  async created() {
    document.title = `修改密碼 || ${config.title}`;
    if (!(await api.is_login())) this.$router.go(-1);
  },
  methods: {
    async submit() {
      if (
        !(this.pass.length && this.pass_rep.length && this.original_pass) ||
        this.pass != this.pass_rep
      ) {
        this.$store.commit("show_popup", { s: "err", msg: "輸入密碼不一致" });
        return false;
      }
      try {
        await api.change_password(this.original_pass, this.pass);
        this.$store.commit("show_popup", { s: "success", msg: "修改成功" });
      } catch {
        this.$store.commit("show_popup", { s: "err", msg: "密碼錯誤" });
      }
    },
  },
};
</script>
