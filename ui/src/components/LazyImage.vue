<template>
  <v-img
    :src="src"
    :lazy-src="lazy_load_src"
    class="grey lighten-2"
    max-width="800px"
  >
    <template v-slot:placeholder>
      <v-row class="fill-height ma-0" align="center" justify="center">
        <v-progress-circular
          indeterminate
          color="grey lighten-5"
        ></v-progress-circular>
      </v-row>
    </template>
  </v-img>
</template>
<script>
import api from "@/api";
export default {
  props: ["src"],
  data: () => ({
    lazy_load_src: "",
  }),
  created() {
    this.lazy_load_src = api.lazy_load_img(this.src);
  },
};
</script>