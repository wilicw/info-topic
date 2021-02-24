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
                label="編號"
                required
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="topic.title"
                :counter="20"
                label="專題名稱"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                v-model="topic.teacher"
                :items="all_teachers"
                label="指導老師"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                multiple
                chips
                dense
                v-model="topic.students"
                :items="classmates"
                label="組員"
                required
              ></v-select>
            </v-col>
          </v-row>
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

export default {
  name: "New",
  data: () => ({
    loading: true,
    all_teachers: [],
    topic: {},
  }),
  async created() {
    if (!(await api.is_login())) this.$router.go(-1);
    document.title = `建立專題 || 大安資訊專題網`;
    let res = await api.get_teachers();
    this.all_teachers = _.flatMap(res.data, (i) => {
      return [i.name];
    });
    res = await api.get_classmates_by_token();
    this.classmates = _.flatMap(res.data.data, (i) => {
      return [i.name];
    });
    this.loading = false;
  },
  methods: {
    async submit() {
      await api.new_topic(this.topic);
      console.log(this.topic);
    },
  },
};
</script>
