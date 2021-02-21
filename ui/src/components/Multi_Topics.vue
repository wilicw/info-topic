<template>
  <div>
    <v-card flat style="background-color: transparent">
      <v-btn plain @click="expand_menu">
        <v-icon class="mr-2">mdi-filter-variant</v-icon> 過濾條件
      </v-btn>
    </v-card>
    <v-expand-transition>
      <v-card v-show="filter_menu" class="mt-2" transition="scale-transition">
        <v-card-text>
          <p class="subtitle-1 mb-2 font-weight-medium">年度</p>
          <div v-for="y in available.years" :key="y" style="display: inline">
            <Chip_checkbox
              v-model="selected.years"
              class="mx-1 my-1"
              :label="y"
              @click.native="update_menu"
            />
          </div>
          <br />
          <p class="subtitle-1 mb-2 font-weight-medium">關鍵字</p>
          <div
            v-for="word in available.keywords"
            :key="word"
            style="display: inline"
          >
            <Chip_checkbox
              v-model="selected.keywords"
              class="mx-1 my-1"
              :label="word"
              @click.native="update_menu"
            />
          </div>
        </v-card-text>
      </v-card>
    </v-expand-transition>
    <br />
    <v-row v-if="topics.length">
      <v-col
        v-for="topic in compinent_topics"
        :key="topic.id"
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
  </div>
</template>

<script>
import _ from "lodash";
import Topic_card from "@/components/Topic_card.vue";
import Chip_checkbox from "@/components/Chip_checkbox.vue";

export default {
  name: "Search_topics",
  props: ["topics"],
  components: {
    Topic_card,
    Chip_checkbox,
  },
  data: () => ({
    compinent_topics: null,
    original_data: null,
    available: {
      years: [],
      keywords: [],
    },
    selected: {
      years: [],
      keywords: [],
    },
    filter_menu: false,
  }),
  watch: {
    topics: {
      handler: function () {
        this.compinent_topics = this.topics;
      },
      immediate: true,
    },
  },
  methods: {
    get_available_options() {
      let years = [];
      _.forEach(this.compinent_topics, (i) => years.push(i.year));
      this.available.years = _.reverse(_.uniq(years).sort());
      this.selected.years = _.cloneDeep(this.available.years);

      let keywords = [];
      _.forEach(
        this.compinent_topics,
        (i) => (keywords = _.concat(keywords, i.keywords))
      );
      this.available.keywords = _.uniq(keywords).sort();
      this.selected.keywords = _.cloneDeep(this.available.keywords);
    },
    expand_menu() {
      this.filter_menu = !this.filter_menu;
      if (this.original_data == null) {
        this.original_data = [];
        _.forEach(this.compinent_topics, (i) => {
          i.keywords = i.keywords.length ? i.keywords : [""];
          this.original_data.push(i);
        });
        this.get_available_options();
      }
    },
    update_menu() {
      console.log("update");
      this.compinent_topics = _.filter(
        this.original_data,
        (i) =>
          _.intersection(this.selected.years, [i.year]).length != 0 &&
          _.intersection(this.selected.keywords, i.keywords).length != 0
      );
    },
  },
};
</script>
