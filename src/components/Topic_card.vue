<template>
  <v-card flat class="rounded-0 mt-5 hover">
    <v-img :src="cover"></v-img>
    <v-chip class="mt-3 ml-3 rounded-0 font-weight-bold" label small dark>{{
      year
    }}</v-chip>
    <v-card-title class="font-weight-bold">{{ title }}</v-card-title>
    <v-card-text>{{ text_truncate(description) }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "Topic_card",
  props: ["title", "cover", "year", "description"],
  data: () => ({
    max_text_turncate: 100,
  }),
  methods: {
    text_truncate(text) {
      if (text.length > this.max_text_turncate) {
        return text.slice(0, this.max_text_turncate) + "...";
      }
      return text;
    },
  },
};
</script>
