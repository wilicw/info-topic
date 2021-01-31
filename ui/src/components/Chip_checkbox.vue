<template>
  <v-chip
    @click="select"
    class="rounded-0 mx-0 my-0"
    :outlined="!is_selected"
    :color="is_selected ? 'primary' : 'grey'"
    >{{ label.toString().length ? label : "無標籤" }}</v-chip
  >
</template>

<script>
import _ from "lodash";

export default {
  name: "chip_checkbox",
  props: ["value", "label"],
  data: () => ({
    is_selected: true,
  }),
  methods: {
    select() {
      let now_value = this.value;
      if (_.indexOf(now_value, this.label) == -1) {
        now_value = _.concat(now_value, this.label);
        this.is_selected = true;
      } else {
        _.remove(now_value, (i) => i == this.label);
        this.is_selected = false;
      }
      console.log(now_value.length);
      this.$emit("input", now_value);
    },
  },
};
</script>
