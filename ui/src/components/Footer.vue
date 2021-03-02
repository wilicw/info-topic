<template>
  <v-card flat class="text-center ma-10 transparent">
    <v-card-text>
      Made with Liver by
      <a
        v-for="author in authors"
        :key="author.name"
        :href="author.link"
        target="_blank"
        >{{ author.name }}</a
      >
      <p></p>
      © {{ new Date().getFullYear() }}
      <strong v-for="o in org" :key="o.name"
        ><a :href="o.link" target="_blank">{{ o.name }}</a></strong
      >
      - All rights reserved.
    </v-card-text>
  </v-card>
</template>

<script>
import { config } from "@/../config";
export default {
  name: "Footer",
  data: () => ({
    authors: [],
    org: [],
  }),
  created() {
    this.authors = config.authors;
    this.org = config.org;
  },
};
</script>
