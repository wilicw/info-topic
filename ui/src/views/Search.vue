<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="6">
        <v-card class="rounded-0 pa-5" :flat="$vuetify.breakpoint.mobile">
          <v-card-title class="font-weight-bold">搜尋專題</v-card-title>
          <v-card-text>
            <br />
            <v-text-field
              v-model="keywords"
              label="關鍵字"
              required
            ></v-text-field>
            <v-row>
              <v-col
                cols="6"
                sm="3"
                v-for="c in search_options"
                :key="c.value"
                class="my-0"
              >
                <v-checkbox
                  v-model="columns"
                  :label="c.text"
                  :value="c.value"
                  class="my-0"
                ></v-checkbox
              ></v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="search">送出</v-btn>
          </v-card-actions>
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
    columns: [],
    search_options: [
      {
        text: "專題名稱",
        value: "name",
      },
      {
        text: "學生",
        value: "student",
      },
      {
        text: "指導老師",
        value: "teacher",
      },
      {
        text: "摘要",
        value: "abstract",
      },
    ],
  }),
  methods: {
    search() {
      const keywords = this.keywords;
      this.$router.push(`/search/${keywords}`);
    },
  },
};
</script>
