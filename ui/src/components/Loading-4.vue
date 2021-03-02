<template>
  <v-row class="mt-5">
    <v-col v-for="i in [0, 1, 2, 3, 4, 5, 6, 7]" :key="i" cols="12" sm="3">
      <v-card>
        <v-skeleton-loader
          type="image, list-item-three-line"
        ></v-skeleton-loader>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "Loading-4",
};
</script>
