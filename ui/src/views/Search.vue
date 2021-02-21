<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="6">
        <v-card class="rounded-0 pa-5" :flat="$vuetify.breakpoint.mobile">
          <v-card-title class="font-weight-bold">搜尋專題</v-card-title>
          <v-form @submit.prevent="search">
            <v-card-text>
              <v-text-field
                v-model="keywords"
                label="關鍵字"
                prepend-icon="mdi-magnify"
                pre-icon="required"
                class="mt-5"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" type="submit">送出</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Search",
  data: () => ({
    keywords: "",
  }),
  created() {
    document.title = `搜尋 || 大安資訊專題網`;
  },
  methods: {
    search() {
      const keywords = this.keywords;
      if (keywords.length != 0) this.$router.push(`/search/${keywords}`);
      return;
    },
  },
};
</script>
