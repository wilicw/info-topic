<template>
  <v-row v-if="topics.length">
    <v-col v-for="topic in topics" :key="topic.id" cols="12" sm="4" md="3">
      <Topic_card
        :uuid="topic.uuid"
        :title="topic.title"
        :year="topic.year"
        :description="topic.description"
        :cover="topic.cover"
      />
    </v-col>
  </v-row>
</template>

<script>
import Topic_card from "@/components/Topic_card.vue";

export default {
  name: "Search_topics",
  props: ["topics"],
  components: {
    Topic_card,
  },
};
</script>
