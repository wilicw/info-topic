<template>
  <v-container>
    <Loading v-if="loading" />
    <div v-else>
      <p class="title font-weight-bold mt-10 mb-0">關鍵字：{{ word }}</p>
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
    </div>
  </v-container>
</template>

<script>
import Loading from "@/components/Loading-4.vue";
import Multi_Topics from "@/components/Multi_Topics.vue";
import api from "@/api";

export default {
  name: "Keyword",
  components: {
    Loading,
    Multi_Topics,
  },
  data: () => ({
    loading: true,
    word: "",
    err: null,
    topics: [],
  }),
  async created() {
    const word = decodeURIComponent(this.$route.params.word);
    console.log(word);
    document.title = `關鍵字 ${word} || 大安資訊專題網`;
    const res = await api.get_topics_by_keyword(word);
    this.topics = res.data;
    this.word = word;
    this.err = !this.topics.length;
    this.loading = false;
  },
};
</script>
