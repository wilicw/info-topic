<template>
  <v-container>
    <br />
    <v-select
      :items="year_list"
      label="選擇年度"
      @change="change_year($event)"
    ></v-select>
    <Loading v-if="loading" />
    <div v-else class="mt-5">
      <Multi_Topics :title="`${year} 級畢業專題`" :topics="topics" />
    </div>
  </v-container>
</template>

<script>
import _ from "lodash";
import Loading from "@/components/Loading-4.vue";
import Multi_Topics from "@/components/Multi_Topics.vue";
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "Year_topics",
  components: {
    Loading,
    Multi_Topics,
  },
  data: () => ({
    loading: true,
    year: "",
    topics: [],
    year_list: [],
  }),
  async created() {
    let res = await api.get_all_year();
    this.year_list = _.reverse(res.data);
    let year = this.$route.params.y;
    if (year == "latest") {
      year = this.year_list[0];
    }
    this.change_year(year);
  },
  methods: {
    change_year: async function (year) {
      this.$router.push(`/year/${year}`);
      this.loading = true;
      this.year = year;
      const res = await api.get_topics_by_year(year);
      this.topics = res.data;
      document.title = `${year} 年專題 || ${config.title}`;
      this.topics = _.shuffle(this.topics);
      this.loading = false;
    },
  },
};
</script>
