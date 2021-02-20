<template>
  <v-row class="mt-5">
    <v-col v-for="i in [0, 1, 2, 3]" :key="i">
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