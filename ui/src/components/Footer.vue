<template>
  <v-card flat class="text-center ma-10 transparent">
    <v-card-text>
      Made with Liver by
      <a
        v-for="author in authors"
        :key="author.name"
        :href="author.link"
        target="_blank"
        class="ml-1"
        >{{ author.name }}</a
      >
      <p class="mt-3">
        <a
          href="https://github.com/wilicw/info-topic"
          title="Go to GitHub repo"
          target="_blank"
          ><img
            src="https://img.shields.io/static/v1?label=wilicw&message=info-topic&color=lightgrey&logo=github"
            alt="wilicw - info-topic"
        /></a>
      </p>
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
