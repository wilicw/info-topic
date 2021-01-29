<template>
  <v-container>
    <p class="title font-weight-bold mt-10" v-if="teacher_name">
      指導老師：{{ teacher_name }}
    </p>
    <v-row>
      <v-col v-for="topic in topics" :key="topic.id" cols="12" sm="4" md="3">
        <Topic_card
          :title="topic.title"
          :year="topic.year"
          :description="topic.description"
          :cover="topic.cover"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import _ from "lodash";
import Topic_card from "@/components/Topic_card.vue";
import api from "@/api";

export default {
  name: "Teachers_topics",
  components: {
    Topic_card,
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
    console.log(this.topics);
    this.topics = _.shuffle(this.topics);
  },
};
</script>
