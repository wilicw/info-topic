<template>
  <v-container id="all_topics">
    <p class="display-1 font-weight-bold">瀏覽專題</p>
    <Loading v-if="loading" />
    <div v-else>
      <v-row>
        <v-col
          v-for="topic in topics"
          :key="topic.title"
          cols="12"
          sm="4"
          md="3"
        >
          <Topic_card
            :uuid="topic.uuid"
            :title="topic.title"
            :year="topic.year"
            :description="topic.description"
            :cover="topic.cover"
          />
        </v-col>
      </v-row>

      <div class="text-center mt-15">
        <v-btn
          @click="
            $router.push('/year/latest');
            $vuetify.goTo(0);
          "
          class="primary"
          >瀏覽更多</v-btn
        >
      </div>
    </div>
  </v-container>
</template>

<script>
import _ from "lodash";
import api from "@/api";
import Topic_card from "@/components/Topic_card.vue";
import Loading from "@/components/Loading-4.vue";

export default {
  name: "Random",
  components: {
    Topic_card,
    Loading,
  },
  data: () => ({
    loading: true,
    topics: [],
  }),
  async created() {
    const res = await api.get_random();
    this.topics = res.data;
    this.topics = _.shuffle(this.topics);
    this.loading = false;
  },
};
</script>
