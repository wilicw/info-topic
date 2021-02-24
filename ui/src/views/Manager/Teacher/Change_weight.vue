<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="6">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">修改分數權重</v-card-title>
            <v-alert
              :value="err"
              color="pink"
              dark
              border="right"
              icon="mdi-close"
              transition="scale-transition"
            >
              發生錯誤
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
              <v-select
                :items="year_list"
                v-model="selected_year"
                label="年度"
              ></v-select>
              <div v-if="selected_year != ''">
                <v-divider></v-divider>
                <br />
                <v-text-field
                  v-for="item in score_data[selected_year]"
                  :key="item.id"
                  v-model="item.weight"
                  :rules="rules"
                  @change="
                    push_change(
                      selected_year,
                      item.score_classification_id,
                      item.weight
                    )
                  "
                  :label="
                    classification_id_to_text(item.score_classification_id)
                  "
                ></v-text-field>
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

export default {
  name: "Change_weight",
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
    document.title = `修改分數權重 || 大安資訊專題網`;
    if (!(await api.is_login())) this.$router.go(-1);
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
  methods: {
    classification_id_to_text(id) {
      return _.find(this.classification, { id: id }).description;
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
