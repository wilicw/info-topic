<template>
  <v-container>
    <Highlight />
    <br />
    <v-divider></v-divider>
    <br />
    <All />
    <br />
    <v-divider></v-divider>
    <br />
    <Footer />
  </v-container>
</template>

<script>
import Highlight from "@/components/Highlight.vue";
import All from "@/components/All.vue";
import Footer from "@/components/Footer.vue";
export default {
  name: "Home",
  components: {
    Highlight,
    All,
    Footer,
  },
};
</script>
