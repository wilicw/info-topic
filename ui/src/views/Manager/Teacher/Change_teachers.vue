<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="10">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">編輯指導老師</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="2">
                  <p class="pt-5 subtitle-1">姓名</p>
                </v-col>
                <v-col cols="2">
                  <p class="pt-5 subtitle-1">是否顯示</p>
                </v-col>
                <v-col cols="8">
                  <p class="pt-5 subtitle-1">說明</p>
                </v-col>
              </v-row>
              <div v-for="t in teachers" :key="t.id">
                <v-divider></v-divider>
                <v-row>
                  <v-col cols="2">
                    <p class="pt-5 body-1">{{ t.name }}</p>
                  </v-col>
                  <v-col cols="2">
                    <v-switch
                      inset
                      v-model="t.enable"
                      @change="change({ id: t.id, enable: t.enable })"
                    ></v-switch>
                  </v-col>
                  <v-col cols="8">
                    <v-text-field
                      class="pt-3"
                      :rules="rules"
                      v-model="t.description"
                      @change="change({ id: t.id, description: t.description })"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="submit()">送出</v-btn>
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
  name: "Change_teachers",
  data: () => ({
    teachers: [],
    changed: [],
    rules: [(value) => !!value || "此欄位不可空白！"],
  }),
  async created() {
    document.title = `編輯指導老師 || ${config.title}`;
    if (!(await api.is_login())) this.$router.go(-1);
    this.init();
  },
  methods: {
    async init() {
      let res;
      try {
        res = await api.get_teachers(true);
        this.teachers = res.data;
      } catch (error) {
        console.log(error);
        this.$router.go(-1);
        return;
      }
    },
    change(data) {
      this.changed.push(data)
    },
    async submit() {
      try {
        await api.edit_teachers(this.changed);
        this.$store.commit("show_popup", { s: "success", msg: "編輯成功" });
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "編輯失敗" });
      }
    }
  },
};
</script>
