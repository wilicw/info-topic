<template>
  <v-container>
    <v-btn
      class="next_btn float_btn"
      v-if="!$vuetify.breakpoint.mobile"
      icon
      fab
      small
      absolute
      top
      right
      @click="next_topic()"
    >
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>

    <v-btn
      class="pre_btn float_btn"
      v-if="!$vuetify.breakpoint.mobile"
      icon
      fab
      small
      absolute
      top
      left
      @click="pre_topic()"
    >
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>
    <v-row
      align="center"
      justify="center"
      class="mt-5"
      style="min-height: 80vh"
    >
      <v-col cols="10" md="5" class="mx-10">
        <p class="subtitle-1 mb-5 ml-1">{{ topic.year }} 級專題製作</p>
        <h1 class="display-3 font-weight-bold mb-7">
          {{ topic.title }}
        </h1>
        <p class="subheading font-weight-regular">
          {{ text_truncate(topic.description) }}
        </p>
        <span
          @click="$router.push(`topic/${topic.uuid}`)"
          class="grey--text hover"
          >檢視完整專題</span
        >
      </v-col>
      <v-col
        cols="12"
        md="5"
        class="mx-10"
        :order="$vuetify.breakpoint.mobile ? 'first' : 'last'"
      >
        <v-img
          transition="scale-transition"
          :alt="topic.title"
          contain
          :src="topic.cover"
          class="cover"
          :max-height="$vuetify.breakpoint.mobile ? '20em' : '45em'"
          v-touch="{
            left: () => next_topic(),
            right: () => pre_topic(),
          }"
        />
      </v-col>
    </v-row>
    <div style="text-align: right" class="floating mx-0">
      <span
        class="mt-3 hover body-2 grey--text"
        @click="$vuetify.goTo('#all_topics')"
      >
        更多專題 <v-icon>mdi-chevron-double-down</v-icon>
      </span>
    </div>
  </v-container>
</template>

<script>
import api from "@/api";
import _ from "lodash";
export default {
  name: "Highlight",
  data: () => ({
    max_text_turncate: 130,
    highlight_topics_id: 0,
    topic: {},
    highlight_topics: [],
  }),
  async created() {
    const res = await api.get_highlight();
    this.highlight_topics = res.data;
    this.highlight_topics_id = _.random(0, this.highlight_topics.length - 1);
    this.topic = this.highlight_topics[this.highlight_topics_id];
  },
  methods: {
    next_topic() {
      const now_id = this.highlight_topics_id;
      this.highlight_topics_id =
        now_id + 1 == this.highlight_topics.length ? 0 : now_id + 1;
      this.topic = this.highlight_topics[this.highlight_topics_id];
    },
    pre_topic() {
      const now_id = this.highlight_topics_id;
      this.highlight_topics_id =
        now_id == 0 ? this.highlight_topics.length - 1 : now_id - 1;
      this.topic = this.highlight_topics[this.highlight_topics_id];
    },
    text_truncate(text) {
      if (text.length > this.max_text_turncate) {
        return text.slice(0, this.max_text_turncate) + "...";
      }
      return text;
    },
    random_rotate() {
      return `transform: rotate(${_.random(-5, 5)}deg);`;
    },
  },
};
</script>
<style scoped>
.float_btn {
  top: 45vh !important;
}

.next_btn {
  right: 3em;
}

.pre_btn {
  left: 3em;
}

.cover {
  filter: drop-shadow(0.35rem 0.35rem 0.4rem rgba(0, 0, 0, 0.5));
}

.floating {
  animation-name: floating;
  animation-duration: 2s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

@keyframes floating {
  100%,
  0% {
    transform: translate(0, 0px);
  }
  50% {
    transform: translate(0, 15px);
  }
}
</style>