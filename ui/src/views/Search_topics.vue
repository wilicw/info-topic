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
    <Multi_Topics :topics="topics" />
  </v-container>
</template>

<script>
import Multi_Topics from "@/components/Multi_Topics.vue";
import api from "@/api";

export default {
  name: "Search_topics",
  components: {
    Multi_Topics,
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
