<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">編輯專題</v-card-title>
            <v-snackbar v-model="err" timeout="2000" color="pink">
              發生錯誤
            </v-snackbar>
            <v-snackbar v-model="success" timeout="2000" color="success">
              儲存成功
            </v-snackbar>
            <v-card-text>
              <v-select
                :items="year_list"
                @change="selected_year"
                label="年度"
              ></v-select>
              <v-expansion-panels focusable>
                <v-expansion-panel v-for="c in stu_class" :key="c">
                  <v-expansion-panel-header>{{
                    id_to_classname(c)
                  }}</v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <br />
                    <p
                      v-for="topic in topics[c]"
                      :key="topic.id"
                      class="title hover"
                      @click="$router.push(`edit/${topic.id}`)"
                    >
                      {{ topic.title }}
                    </p>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-text>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import _ from "lodash";
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "Score",
  data: () => ({
    err: null,
    success: null,
    year_list: [],
    students: [],
    stu_class: [],
    changed: [],
    rules: [
      (value) =>
        (!!value && !isNaN(value) && parseInt(value) >= 0) ||
        "此欄位不可空白且需為 0 或正整數！",
    ],
  }),
  async created() {
    document.title = `編輯所有專題 || ${config.title}`;
    if (!(await api.is_login())) this.$router.go(-1);
    let res;
    try {
      res = await api.get_all_year();
      this.year_list = res.data;
      this.year_list = _.reverse(this.year_list.sort());
    } catch (error) {
      console.log(error);
      this.$router.go(-1);
      return;
    }
  },
  methods: {
    id_to_classname(id) {
      switch (id) {
        case "A":
          return "甲班";
        case "B":
          return "乙班";
        default:
          return "綜高";
      }
    },
    async submit() {},
    async selected_year(value) {
      const res = await api.get_topics_by_year(value);
      this.topics = _.groupBy(res.data, (i) => {
        return i.uuid.slice(-3, -2);
      });
      this.stu_class = _.keys(this.topics);
      this.stu_class = this.stu_class.sort();
    },
  },
};
</script>
