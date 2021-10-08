<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="5">
        <Score_classification
          :classification="classification"
          :fetch="() => this.init()"
        />
      </v-col>
      <v-col cols="12" md="6">
        <Score_weight
          :score_data="score_data"
          :year_list="year_list"
          @new_year="new_year"
          :classification="classification"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import _ from "lodash";
import api from "@/api";
import { config } from "@/../config";
import Score_classification from "@/components/Score_classification.vue";
import Score_weight from "@/components/Score_weight.vue";

export default {
  name: "Change_weight",
  components: {
    Score_classification,
    Score_weight,
  },
  data: () => ({
    classification: [],
    score_data: [],
    year_list: [],
    selected_year: "",
    changed: [],
    rules: [
      (value) =>
        (!!value && !isNaN(value) && parseInt(value) >= 0) ||
        "此欄位不可空白且需為 0 或正整數！",
    ],
  }),
  async created() {
    document.title = `修改分數選項 || ${config.title}`;
    if (!(await api.is_login())) this.$router.go(-1);
    this.init();
  },
  methods: {
    async init() {
      let res;
      try {
        res = await api.get_score_weight();
        this.score_data = res.data;
        res = await api.get_score_classification();
        this.classification = res.data;
      } catch (error) {
        console.log(error);
        this.$router.go(-1);
        return;
      }
      this.score_data = _.groupBy(this.score_data, "year");
      this.year_list = _.keys(this.score_data);
      this.year_list = _.uniq(this.year_list);
      this.year_list = _.reverse(this.year_list.sort());
    },
    new_year(y) {
      this.year_list.push(y);
      this.year_list = _.uniq(this.year_list);
      this.year_list = _.reverse(this.year_list.sort());
    },
  },
};
</script>
