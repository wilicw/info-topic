<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="4">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form @submit.prevent="submit">
            <v-card-title class="font-weight-bold">修改密碼</v-card-title>
            <v-alert
              :value="err"
              color="pink"
              dark
              border="right"
              icon="mdi-close"
              transition="scale-transition"
            >
              密碼錯誤
            </v-alert>
            <v-alert
              :value="success"
              color="green"
              dark
              border="right"
              icon="mdi-check"
              transition="scale-transition"
            >
              修改成功
            </v-alert>
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

export default {
  name: "Change_password",
  data: () => ({
    original_pass: "",
    pass: "",
    pass_rep: "",
    err: null,
    success: null,
    rules: [(value) => !!value || "此欄位不可空白！"],
  }),
  async created() {
    document.title = `修改密碼 || 大安資訊專題網`;
    if (!(await api.is_login())) this.$router.go(-1);
  },
  methods: {
    async submit() {
      if (
        !(this.pass.length && this.pass_rep.length && this.original_pass) ||
        this.pass != this.pass_rep
      ) {
        this.err = true;
        this.success = null;
        return false;
      }
      let res;
      try {
        res = await api.change_password(this.original_pass, this.pass);
        if (res.status == 200) {
          this.err = null;
          this.success = true;
        }
      } catch {
        this.err = true;
        this.success = null;
      }
    },
  },
};
</script>
