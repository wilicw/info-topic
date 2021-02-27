<template>
  <v-dialog width="500" v-model="dialog">
    <template v-slot:activator="{ on, attrs }">
      <v-btn small icon v-bind="attrs" v-on="on">
        <v-icon small>{{ icon }}</v-icon>
      </v-btn>
    </template>

    <v-card class="py-3">
      <v-card-title class="title">{{ title }} </v-card-title>
      <v-card-text>
        <br />
        <v-text-field v-model="__description" label="分類說明"></v-text-field>
        <v-checkbox v-model="__global" label="組別分數"></v-checkbox>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          class="primary"
          @click="
            action({ description: __description, global: __global });
            dialog = false;
          "
          >儲存</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Edit_score_classification",
  props: ["title", "action", "icon", "description", "global"],
  data: () => ({
    dialog: false,
    __description: "",
    __global: false,
  }),
  created() {
    this.__description = this.description;
    this.__global = this.global;
  },
};
</script>
