<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">評分</v-card-title>
            <v-card-text>
              <v-select
                :items="year_list"
                @change="selected_year"
                label="年度"
              ></v-select>
              <v-expansion-panels focusable>
                <v-expansion-panel v-for="topic in selected_projects" :key="topic.id">
                  <v-expansion-panel-header @click="students_in_topic(topic.uuid)">
                    {{ topic.title }}
                    <span class="text--secondary mx-1"> {{ topic.uuid }}</span>
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <div
                      style="overflow-x: auto; overflow-y: hidden; white-space: nowrap"
                    >
                      <br />

                      <v-row>
                        <v-col v-for="score in project_classification" :key="score.id">
                          <v-text-field
                            @change="push_changed($event, score.id, -1, topic.uuid)"
                            :value="get_topic_score(topic.uuid, score.id)"
                            :label="score.description"
                            :rules="rules"
                            disabled
                          ></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col>
                          <p class="mt-4 ml-4 subtitle-1">姓名</p>
                        </v-col>
                        <v-col v-for="c in classification" :key="c.id">
                          <p class="mt-4 ml-4 subtitle-1">
                            {{ c.description }}
                          </p>
                        </v-col>
                      </v-row>
                      <v-row
                        v-for="(s, i) in students"
                        :key="s.id"
                        :class="
                          $vuetify.theme.dark
                            ? {
                                'grey darken-2': i % 2 == 0,
                                'grey darken-3': i % 2,
                              }
                            : {
                                'grey lighten-2': i % 2 == 0,
                                'grey lighten-3': i % 2,
                              }
                        "
                      >
                        <v-col>
                          <p class="mt-4 ml-4 subtitle-1">{{ s.name }}</p>
                        </v-col>
                        <v-col v-for="c in classification" :key="c.id">
                          <v-text-field
                            @change="push_changed($event, c.id, s.id)"
                            :value="get_score_by_classification(s.scores, c.id)"
                            :rules="rules"
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
                    </div>
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
import { config } from "@/../config";

export default {
  name: "Score",
  data: () => ({
    classification: [],
    year_list: [],
    selected_projects: [],
    topics: [],
    students: [],
    changed: [],
    project_classification: [],
    rules: [
      (value) => (!!value && !isNaN(value) && parseInt(value) >= 0) || "此欄位不可空白！",
    ],
  }),
  async created() {
    document.title = `評分 || ${config.title}`;
    if (!(await api.is_login())) this.$router.go(-1);
    let res;
    try {
      res = await api.get_score_classification();
      const all_classification = res.data;
      this.project_classification = _.filter(all_classification, {
        global: true,
      });
      this.classification = _.filter(all_classification, {
        global: false,
      });
      this.classification = _.sortBy(this.classification, ["id"]);
      res = await api.get_topic_by_token();
      this.topics = res.data;
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
        this.$store.commit("show_popup", { s: "success", msg: "儲存成功" });
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "發生錯誤" });
      }
      this.$vuetify.goTo(0);
    },
    async selected_year(value) {
      this.selected_projects = _.filter(this.topics, { year: value });
      console.log(this.selected_projects);
    },
    async students_in_topic(uuid) {
      const res = await api.get_students_by_topic(uuid);
      this.students = res.data;
      this.students = _.sortBy(this.students, ["id"]);
    },
    get_score_by_classification(scores, id) {
      console.log(scores);
      const s = _.head(_.filter(scores, { score_classification_id: id }));
      return s == undefined ? "" : s.score;
    },
    download(link) {
      console.log(link);
      window.open(link, "_blank");
    },
    push_changed(score, classification_id, student_id, uuid = null) {
      if (this.rules[0](score) != true) return;
      _.remove(this.changed, {
        classification_id: classification_id,
        student_id: student_id,
      });
      this.changed.push({
        student_id: student_id,
        score: parseInt(score),
        classification_id: classification_id,
        uuid: uuid === null ? -1 : uuid,
      });
      console.log(this.changed);
    },
    get_topic_score(uuid, classification_id) {
      const topic = _.head(_.filter(this.topics, { uuid: uuid }));
      const score = _.head(
        _.filter(topic.score, { score_classification_id: classification_id })
      );
      return score == undefined ? "尚未評分" : score.score;
    },
  },
};
</script>
