<template>
  <v-container>
    <Loading v-if="loading" />
    <div v-else>
      <p class="title font-weight-bold mt-10" v-if="teacher_name">
        指導老師：{{ teacher_name }}
      </p>
      <Multi_Topics :topics="topics" />
    </div>
  </v-container>
</template>

<script>
import _ from "lodash";
import Loading from "@/components/Loading-4.vue";
import Multi_Topics from "@/components/Multi_Topics.vue";
import api from "@/api";

export default {
  name: "Teachers_topics",
  components: {
    Loading,
    Multi_Topics,
  },
  data: () => ({
    loading: true,
    teacher_name: "",
    topics: [],
  }),
  async created() {
    const teacher_id = this.$route.params.id;
    const res = await api.get_topics_by_tid(teacher_id);
    this.topics = res.data.projects;
    this.teacher_name = res.data.name;
    document.title = `指導老師 ${this.teacher_name} || 大安資訊專題網`;
    this.topics = _.shuffle(this.topics);
    this.loading = false;
  },
};
</script>
