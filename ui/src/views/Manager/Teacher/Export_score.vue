<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">匯出總成績</v-card-title>
            <v-card-text>
              <v-select
                :items="year_list"
                v-model="selected_year"
                label="年度"
              ></v-select>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                @click="download"
                :loading="loading"
                :disabled="selected_year == ''"
                color="primary"
                ><v-icon small>mdi-download</v-icon> 下載 csv</v-btn
              >
            </v-card-actions>
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
    loading: null,
    selected_year: "",
    year_list: [],
  }),
  async created() {
    document.title = `匯出總成績 || ${config.title}`;
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
    async download() {
      this.loading = true;
      try {
        let response = await api.export_score(this.selected_year);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `${this.selected_year}級學生總成績.csv`);
        document.body.appendChild(link);
        link.click();
        this.$store.commit("show_popup", { s: "success", msg: "匯出成功" });
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "匯出失敗" });
      }
      this.loading = false;
    },
  },
};
</script>
