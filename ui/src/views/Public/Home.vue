<template>
  <v-container>
    <Highlight />
    <br />
    <v-divider></v-divider>
    <br />
    <All />
  </v-container>
</template>

<script>
import Highlight from "@/components/Highlight.vue";
import All from "@/components/All.vue";
import { config } from "@/../config";

export default {
  name: "Home",
  components: {
    Highlight,
    All,
  },
  created() {
    document.title = `首頁 || ${config.title}`;
  },
};
</script>
