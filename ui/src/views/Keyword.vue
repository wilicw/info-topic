<template>
  <v-container>
    <p class="title font-weight-bold mt-10">關鍵字：{{ word }}</p>
    <v-alert
      v-if="err"
      color="pink"
      dark
      border="right"
      icon="mdi-alert"
      transition="scale-transition"
    >
      沒有關鍵字為{{ word }}的專題
    </v-alert>
    <Multi_Topics :topics="topics" />
  </v-container>
</template>

<script>
import Multi_Topics from "@/components/Multi_Topics.vue";
import api from "@/api";

export default {
  name: "Keyword",
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
    const res = await api.get_topics_by_keyword(word);
    this.topics = res.data;
    this.word = word;
    this.err = !this.topics.length;
  },
};
</script>
