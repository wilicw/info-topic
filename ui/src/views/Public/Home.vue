<template>
  <v-container>
    <Highlight />
    <br />
    <v-divider></v-divider>
    <br />
    <Random />
  </v-container>
</template>

<script>
import Highlight from "@/components/Highlight.vue";
import Random from "@/components/Random.vue";
import { config } from "@/../config";

export default {
  name: "Home",
  components: {
    Highlight,
    Random,
  },
  created() {
    document.title = `首頁 || ${config.title}`;
  },
};
</script>
