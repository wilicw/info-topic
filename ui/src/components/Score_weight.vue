<template>
  <v-card>
    <v-form>
      <v-card-title class="font-weight-bold">修改分數權重</v-card-title>
      <v-card-text>
        <v-select
          :items="year_list"
          v-model="selected_year"
          label="年度"
        ></v-select>
        <div v-if="selected_year != ''">
          <v-divider></v-divider>
          <v-text-field
            v-for="c in classification"
            :key="c.id"
            :value="get_score_weight(c.id)"
            :rules="rules"
            @change="push_change(selected_year, c.id, $event)"
            :label="c.description + (c.global ? '（組）' : '')"
          ></v-text-field>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="submit()">送出</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template> 

<script>
import _ from "lodash";
import api from "@/api";

export default {
  name: "Change_weight",
  props: ["classification", "score_data", "year_list"],
  data: () => ({
    selected_year: "",
    changed: [],
    rules: [
      (value) =>
        (!!value && !isNaN(value) && parseInt(value) >= 0) ||
        "此欄位不可空白且需為 0 或正整數！",
    ],
  }),
  methods: {
    get_score_weight(classification_id) {
      const score = _.find(this.score_data[this.selected_year], {
        score_classification_id: classification_id,
      });
      return score == undefined ? 0 : score.weight;
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
    async submit() {
      console.log(this.changed);
      try {
        await api.set_score_weight(this.changed);
        this.$store.commit("show_popup", { s: "success", msg: "修改成功" });
        this.changed = [];
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "修改失敗" });
      }
    },
  },
};
</script>
