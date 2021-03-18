<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="10">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">匯入專題分數</v-card-title>
            <v-card-text>
              <v-select
                :items="items"
                v-model="selected_classification"
                label="成績"
              ></v-select>
              <div v-if="selected_classification_id">
                <br />
                <v-divider></v-divider>
                <br />
                <br />
                <v-row>
                  <v-col>
                    <p class="mb-1">組別編號</p>
                    <p class="text--secondary mb-0">
                      已輸入 {{ calcuate_num(group) }} 組
                    </p>
                    <v-textarea auto-grow v-model="group"></v-textarea>
                  </v-col>
                  <v-col>
                    <p class="mb-1">成績</p>
                    <p class="text--secondary mb-0">
                      已輸入 {{ calcuate_num(score) }} 組
                    </p>
                    <v-textarea auto-grow v-model="score"></v-textarea>
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
import _ from "lodash";
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "Change_weight",
  data: () => ({
    classification: [],
    score: "",
    group: "",
    items: [],
    selected_classification_id: null,
    selected_classification: null,
  }),
  watch: {
    selected_classification: function (text) {
      const item = _.find(this.classification, { description: text });
      this.selected_classification_id = item.id;
    },
  },
  async created() {
    document.title = `匯入專題分數 || ${config.title}`;
    if (!(await api.is_login())) this.$router.go(-1);
    if (api.get_group() != "admin") this.$router.go(-1);
    let res;
    try {
      res = await api.get_score_classification();
      this.classification = res.data;
      this.classification = _.filter(this.classification, { global: true });
      this.items = _.map(this.classification, (i) => i.description);
    } catch (error) {
      console.log(error);
      this.$router.go(-1);
      return;
    }
  },
  methods: {
    split_line(text) {
      return text.replace(/(^[ \t]*\n)/gm, "").split("\n");
    },
    calcuate_num(text) {
      return this.split_line(text).length - 1;
    },
    async submit() {
      const group_data = this.group;
      const score_data = this.score;
      if (
        this.calcuate_num(group_data) == 0 ||
        this.calcuate_num(score_data) == 0 ||
        this.calcuate_num(group_data) != this.calcuate_num(score_data)
      ) {
        return;
      }
      try {
        api.import_score(
          this.selected_classification_id,
          this.split_line(group_data),
          this.split_line(score_data)
        );
        this.$store.commit("show_popup", { s: "success", msg: "匯入成功" });
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "匯入失敗" });
      }
    },
  },
};
</script>
