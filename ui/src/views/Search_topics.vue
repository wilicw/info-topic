<template>
  <v-container>
    <p class="title font-weight-bold mt-10">搜尋：{{ word }}</p>
    <v-alert
      v-if="err"
      color="pink"
      dark
      border="right"
      icon="mdi-alert"
      transition="scale-transition"
    >
      沒有關於{{ word }}的專題
    </v-alert>
    <v-row v-if="topics.length">
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
import Topic_card from "@/components/Topic_card.vue";
import api from "@/api";

export default {
  name: "Search_topics",
  components: {
    Topic_card,
  },
  data: () => ({
    word: "",
    err: null,
    topics: [],
  }),
  async created() {
    const word = decodeURIComponent(this.$route.params.word);
    console.log(word);
    const res = await api.get_topics_search(word);
    this.topics = res.data;
    this.word = word;
    this.err = !this.topics.length;
  },
};
</script>
