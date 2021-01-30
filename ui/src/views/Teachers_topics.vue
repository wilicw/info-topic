<template>
  <v-container>
    <p class="title font-weight-bold mt-10" v-if="teacher_name">
      指導老師：{{ teacher_name }}
    </p>
    <Multi_Topics :topics="topics" />
  </v-container>
</template>

<script>
import _ from "lodash";
import Multi_Topics from "@/components/Multi_Topics.vue";
import api from "@/api";

export default {
  name: "Teachers_topics",
  components: {
    Multi_Topics,
  },
  data: () => ({
    teacher_name: "",
    topics: [],
  }),
  async created() {
    const teacher_id = this.$route.params.id;
    const res = await api.get_topics_by_tid(teacher_id);
    this.topics = res.data.projects;
    this.teacher_name = res.data.name;
    this.topics = _.shuffle(this.topics);
  },
};
</script>
