<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">評分</v-card-title>
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
              儲存成功
            </v-alert>
            <v-card-text>
              <v-select
                :items="year_list"
                @change="selected_year"
                label="年度"
              ></v-select>
              <v-expansion-panels focusable>
                <v-expansion-panel
                  v-for="topic in selected_projects"
                  :key="topic.id"
                >
                  <v-expansion-panel-header
                    @click="students_in_topic(topic.uuid)"
                  >
                    {{ topic.title }}
                    <span class="text--secondary mx-1"> {{ topic.uuid }}</span>
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <br />
                    <v-row class="text-right">
                      <v-col>
                        <v-text-field
                          value="姓名"
                          solo
                          readonly
                          flat
                        ></v-text-field>
                        <v-text-field
                          v-for="stu in students"
                          :key="stu.id"
                          :value="stu.name"
                          solo
                          readonly
                          flat
                        ></v-text-field>
                      </v-col>
                      <v-col v-for="score in classification" :key="score.id">
                        <v-text-field
                          :value="score.description"
                          solo
                          readonly
                          flat
                        ></v-text-field>
                        <v-text-field
                          v-for="s in get_score_by_classification(score.id)"
                          :key="s.student_id"
                          v-model="s.score"
                          class="mt-2"
                          :rules="rules"
                          @change="
                            push_changed(s.score, score.id, s.student_id)
                          "
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-divider class="my-5"></v-divider>
                    <v-row align="center">
                      <v-col>
                        <v-btn
                          plain
                          block
                          @click="download(topic.presentation_file)"
                          :disabled="topic.presentation_file == ''"
                          ><v-icon>mdi-download</v-icon>簡報</v-btn
                        >
                      </v-col>
                      <v-col>
                        <v-btn
                          plain
                          block
                          @click="download(topic.report_file)"
                          :disabled="topic.report_file == ''"
                          ><v-icon>mdi-download</v-icon>報告</v-btn
                        >
                      </v-col>
                      <v-col>
                        <v-btn
                          plain
                          block
                          :disabled="topic.program_file == ''"
                          @click="download(topic.program_file)"
                        >
                          <v-icon>mdi-download</v-icon>程式</v-btn
                        >
                      </v-col>
                    </v-row>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="submit()">儲存</v-btn>
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
  name: "Score",
  data: () => ({
    err: null,
    success: null,
    classification: [],
    year_list: [],
    selected_projects: [],
    topics: [],
    students: [],
    changed: [],
    rules: [
      (value) =>
        (!!value && !isNaN(value) && parseInt(value) >= 0) ||
        "此欄位不可空白且需為 0 或正整數！",
    ],
  }),
  async created() {
    document.title = `評分 || 大安資訊專題網`;
    if (!(await api.is_login())) this.$router.go(-1);
    let res;
    try {
      res = await api.get_score_classification();
      this.classification = res.data.data;
      this.classification = _.sortBy(this.classification, ["id"]);
      res = await api.get_topic_by_token();
      this.topics = res.data.data;
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
    classification_id_to_text(id) {
      return _.find(this.classification, { id: id }).description;
    },
    async submit() {
      try {
        await api.set_score(this.changed);
        this.err = false;
        this.success = true;
      } catch (error) {
        this.err = true;
        this.success = false;
        console.log(error);
      }
      this.$vuetify.goTo(0);
    },
    async selected_year(value) {
      this.selected_projects = _.filter(this.topics, { year: value });
      console.log(value);
    },
    async students_in_topic(uuid) {
      const res = await api.get_students_by_topic(uuid);
      this.students = res.data.data;
      this.students = _.sortBy(this.students, ["id"]);
    },
    get_score_by_classification(id) {
      let result = [];
      this.students.forEach((i) => {
        let o;
        let s = _.head(_.filter(i.scores, { score_classification_id: id }));
        if (s == undefined) {
          o = {
            student_id: i.id,
            score: 0,
            classification_id: id,
          };
        } else {
          o = {
            student_id: i.id,
            score: s.score,
            classification_id: id,
          };
        }
        result.push(o);
      });
      return result;
    },
    download(link) {
      console.log(link);
      window.open(link, "_blank");
    },
    push_changed(score, classification_id, student_id) {
      if (this.rules[0](score) != true) return;
      _.remove(this.changed, {
        classification_id: classification_id,
        student_id: student_id,
      });
      this.changed.push({
        student_id: student_id,
        score: parseInt(score),
        classification_id: classification_id,
      });
    },
  },
};
</script>
