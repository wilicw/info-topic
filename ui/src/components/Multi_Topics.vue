<template>
  <div>
    <div>
      <span class="title font-weight-bold mt-10 mb-0">{{ title }}</span>
      <v-btn
        style="float: right"
        plain
        @click="expand_menu"
        :icon="$vuetify.breakpoint.mobile"
      >
        <v-icon>mdi-filter-variant</v-icon>
        <span v-if="!$vuetify.breakpoint.mobile">過濾條件</span>
      </v-btn>
      <p v-if="filter_menu"></p>
      <v-expand-transition class="mt-2">
        <v-card v-show="filter_menu" width="100%">
          <v-card-text>
            <div v-if="available.years.length > 1">
              <p class="subtitle-1 mb-2 font-weight-medium">年度</p>
              <div
                v-for="y in available.years"
                :key="y"
                style="display: inline"
              >
                <Chip_checkbox
                  v-model="selected.years"
                  class="mx-1 my-1"
                  :label="y"
                  @click.native="update_menu"
                />
              </div>
              <br />
            </div>
            <p class="subtitle-1 mb-2 font-weight-medium">關鍵字</p>
            <div
              v-for="word in available.keywords"
              :key="word"
              style="display: inline"
            >
              <Chip_checkbox
                class="mx-1 my-1"
                v-model="selected.keywords"
                :label="word"
                @click.native="update_menu"
              />
            </div>
          </v-card-text>
        </v-card>
      </v-expand-transition>
    </div>
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
  props: ["title", "topics"],
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
      // this.selected.keywords = _.cloneDeep(this.available.keywords);
      this.selected.keywords = [];
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
      if (this.selected.keywords.length == 0) {
        this.compinent_topics = this.original_data;
      } else {
        this.compinent_topics = _.filter(
          this.original_data,
          (i) =>
            _.intersection(this.selected.years, [i.year]).length != 0 &&
            _.intersection(this.selected.keywords, i.keywords).length != 0
        );
      }
    },
  },
};
</script>
