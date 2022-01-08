<template>
  <v-img :src="src" :lazy-src="lazy_load_src" :class="is_svg ? 'grey lighten-2' : ''">
    <template v-slot:placeholder>
      <v-row class="fill-height ma-0" align="center" justify="center">
        <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
      </v-row>
    </template>
  </v-img>
</template>
<script>
import api from "@/api";
export default {
  props: ["src"],
  data: () => ({
    is_svg: null,
    lazy_load_src: "",
  }),
  created() {
    this.is_svg = this.src.endsWith(".svg");
    this.lazy_load_src = api.lazy_load_img(this.src);
  },
};
</script>
