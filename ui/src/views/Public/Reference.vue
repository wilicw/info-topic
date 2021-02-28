<template>
  <v-row justify="center" class="mt-3">
    <v-col cols="12" lg="8" sm="10">
      <v-card class="rounded-0 mt-5 pa-3">
        <p class="display-1 font-weight-medium mt-3 ml-3">
          <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 參考資料
        </p>
        <div class="mt-10" v-html="ref"></div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "Detail",
  data: () => ({
    loading: true,
    ref: "",
  }),
  async created() {
    document.title = `參考資料 || ${config.title}`;
    try {
      const res = await api.get_reference();
      this.ref = res.data;
    } catch (error) {
      this.ref = ``;
    }
  },
};
</script>

<style scoped>
blockquote {
  margin: 2em;
}
</style>