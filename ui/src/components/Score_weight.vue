<template>
  <v-card>
    <v-form>
      <v-card-title class="font-weight-bold">
        修改分數權重
        <v-spacer></v-spacer>
        <v-btn @click="dialog_new_year = !dialog_new_year" icon small>
          <v-icon small>mdi-plus</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-select :items="year_list" v-model="selected_year" label="年度"></v-select>
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
    <v-dialog v-model="dialog_new_year" max-width="500px">
      <v-card>
        <v-form @submit.prevent="new_year">
          <v-card-title>新增年度</v-card-title>
          <v-card-text>
            <v-text-field label="年度" v-model="new_year_input"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="dialog_new_year = false">取消</v-btn>
            <v-btn
              color="primary"
              :disabled="isNaN(parseInt(new_year_input))"
              type="submit"
              >儲存</v-btn
            >
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import _ from "lodash";
import api from "@/api";

export default {
  name: "Change_weight",
  props: ["classification", "score_data", "year_list"],
  data: () => ({
    dialog_new_year: null,
    new_year_input: new Date().getFullYear() - 1911 + 1,
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
      try {
        await api.set_score_weight(this.changed);
        this.$store.commit("show_popup", { s: "success", msg: "修改成功" });
        this.changed = [];
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "修改失敗" });
      }
    },
    new_year() {
      this.new_year_input = parseInt(this.new_year_input);
      this.$emit("new_year", this.new_year_input);
      this.dialog_new_year = false;
      this.selected_year = this.new_year_input;
    },
  },
};
</script>
