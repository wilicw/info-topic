<template>
  <v-row justify="center" class="mt-2">
    <v-col cols="12" lg="10" sm="10">
      <v-card class="rounded-0 mt-5 pa-10">
        <div v-if="loading">
          <v-skeleton-loader
            type="article, article, article"
          ></v-skeleton-loader>
        </div>
        <div v-else>
          <p class="headline mb-10 font-weight-medium">建立專題</p>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="topic.uuid"
                :rules="rules"
                label="編號"
                required
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="topic.title"
                :counter="20"
                :rules="rules"
                label="專題名稱"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                v-model="topic.teacher"
                :items="all_teachers"
                :rules="rules"
                label="指導老師"
              ></v-select>
            </v-col>
          </v-row>
          <v-card>
            <v-card-text>
              <p>已選擇 {{ topic.students.length }} 位成員</p>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-subheader>選擇班級</v-subheader>
                  <v-btn
                    block
                    text
                    class="my-2 hover subtitle-1"
                    v-for="(item, i) in stu_class"
                    :key="i"
                    @click="selected_class = item"
                  >
                    {{ id_to_classname(item) }}
                  </v-btn>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-subheader>選擇成員</v-subheader>
                  <div v-for="item in classmates" :key="item.id">
                    <v-checkbox
                      v-model="topic.students"
                      :label="item.name"
                      :value="item.id"
                      v-if="
                        selected_class ==
                        item.username.slice(-3, -2).toUpperCase()
                      "
                    >
                    </v-checkbox>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
          <v-card-actions class="mt-10">
            <v-spacer></v-spacer>
            <v-btn @click="submit" class="primary">建立</v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import _ from "lodash";
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "New",
  data: () => ({
    loading: true,
    all_teachers: [],
    stu_class: [],
    stu_in_class: [],
    classmates: [],
    topic: {
      students: [],
    },
    selected_stu: null,
    selected_class: "A",
    rules: [(value) => !!value || "此欄位不可空白！"],
  }),
  async created() {
    if (!(await api.is_login())) this.$router.go(-1);
    document.title = `建立專題 || ${config.title}`;
    let res = await api.get_teachers();
    this.all_teachers = _.flatMap(res.data, (i) => {
      return [i.name];
    });
    const year = api.get_username().slice(0, -3);
    res = await api.get_students_by_year(year);
    this.classmates = res.data;
    this.stu_class = _.map(this.classmates, (i) =>
      i.username.slice(-3, -2).toUpperCase()
    );
    this.stu_class = _.uniq(this.stu_class);
    this.loading = false;
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
    async submit() {
      try {
        await api.new_topic(this.topic);
        this.$store.commit("show_popup", { s: "success", msg: "建立成功" });
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "發生錯誤" });
      }
    },
  },
};
</script>
