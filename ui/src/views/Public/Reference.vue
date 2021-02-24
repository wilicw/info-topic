<template>
  <v-row justify="center" class="mt-3">
    <v-col cols="12" lg="8" sm="10">
      <v-card class="rounded-0 mt-5 pa-3"> <div v-html="ref"></div> </v-card>
    </v-col>
  </v-row>
</template>

<script>
import api from "@/api";

export default {
  name: "Detail",
  data: () => ({
    loading: true,
    ref: "",
  }),
  async created() {
    const res = await api.get_reference();
    this.ref = res.data;
  },
};
</script>
