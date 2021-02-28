<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col v-for="t in teachers" :key="t.id" cols="12" sm="4">
        <v-card class="rounded-0 pa-5 ma-3">
          <v-card-title class="headline font-weight-bold">
            {{ t.name }} <span class="title">老師</span>
          </v-card-title>
          <v-card-text>
            {{ t.description }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="to_teacher_topic(t.name)" plain
              >瀏覽曾經專題內容</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "Teachers",
  data: () => ({
    teachers: [],
  }),
  async created() {
    document.title = `指導老師 || ${config.title}`;
    const res = await api.get_teachers();
    this.teachers = res.data;
  },
  methods: {
    to_teacher_topic(name) {
      this.$router.push(`/teachers/${name}`);
    },
  },
};
</script>
