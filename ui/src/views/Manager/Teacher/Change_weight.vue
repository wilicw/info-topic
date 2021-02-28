<template>
  <v-container>
    <v-snackbar v-model="err" timeout="2000" color="pink">
      發生錯誤
    </v-snackbar>
    <v-snackbar v-model="success" timeout="2000" color="success">
      儲存成功
    </v-snackbar>
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
    err: null,
    success: null,
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
        this.score_data = res.data.data;
        res = await api.get_score_classification();
        this.classification = res.data.data;
      } catch (error) {
        console.log(error);
        this.$router.go(-1);
        return;
      }
      this.score_data = _.groupBy(this.score_data, "year");
      this.year_list = _.keys(this.score_data);
      this.year_list = _.reverse(this.year_list.sort());
    },
    classification_id_to_text(id) {
      const item = _.find(this.classification, { id: id });
      return item.description + (item.global ? "（組）" : "");
    },
    push_change(year, classification_id, weight) {
      if (this.rules[0](weight) != true) {
        return;
      }
      _.remove(this.changed, {
        year: year,
        classification_id: classification_id,
      });
      this.changed.push({
        year: year,
        classification_id: classification_id,
        weight: weight,
      });
    },
    async new_classification(text, global) {
      if (text == "") return;
      await api.create_score_classification(text, global);
      this.init();
    },
    async edit_classification(id, text, global) {
      if (text == "") return;
      await api.update_score_classification(id, text, global);
      this.init();
    },
    async delete_classification(id) {
      await api.delete_score_classification(id);
      this.init();
    },
    async submit() {
      console.log(this.changed);
      try {
        await api.set_score_weight(this.changed);
        this.success = true;
        this.err = false;
        this.changed = [];
      } catch (error) {
        this.success = false;
        this.err = true;
      }
    },
  },
};
</script>
