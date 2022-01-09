<template>
  <v-container>
    <v-img
      class="mx-auto mt-5"
      src="http://thecatapi.com/api/images/get?format=src&type=gif"
    ></v-img>
  </v-container>
</template>

<script>
import { config } from "@/../config";
export default {
  name: "Cat",
  created() {
    document.title = `C@T || ${config.title}`;
  },
};
</script>
