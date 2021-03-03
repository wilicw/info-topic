<template>
  <v-container>
    <br />
    <v-row>
      <v-col>
        <v-select
          :items="year_list"
          label="選擇年度"
          @change="change_year($event)"
        ></v-select>
      </v-col>
      <v-col>
        <v-select
          :items="classification_list"
          label="選擇類別"
          @change="change_classification($event)"
        ></v-select>
      </v-col>
    </v-row>
    <Loading v-if="loading" />
    <div v-else class="mt-5">
      <Multi_Topics
        :title="`${year} 級 - ${classification_description}排名`"
        :topics="topics"
      />
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
  name: "Rank_topics",
  components: {
    Loading,
    Multi_Topics,
  },
  data: () => ({
    loading: true,
    year: "",
    classification_id: null,
    classification_description: "",
    topics: [],
    year_list: [],
    classifications: [],
    classification_list: [],
  }),
  async created() {
    let res = await api.get_all_year();
    this.year_list = _.reverse(res.data);
    res = await api.get_score_classification();
    this.classifications = _.filter(res.data.data, { global: true });
    this.classification_list = _.map(this.classifications, "description");
    let year = this.$route.params.y;
    if (_.indexOf(this.year_list, year) == -1) {
      year = this.year_list[0];
    }
    this.change_classification(this.classification_list[0]);
    this.change_year(year);
  },
  methods: {
    change_year: async function (year) {
      this.$router.push(`/rank/${year}`);
      this.loading = true;
      this.year = year;
      const res = await api.get_topics_by_classification(
        year,
        this.classification_id
      );
      this.topics = res.data;
      document.title = `${year} 年度專題排名 || ${config.title}`;
      this.loading = false;
    },
    change_classification(text) {
      const c = _.head(_.filter(this.classifications, { description: text }));
      this.classification_id = c.id;
      this.classification_description = c.description;
      this.change_year(this.year);
    },
  },
};
</script>
