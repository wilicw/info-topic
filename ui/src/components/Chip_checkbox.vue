<template>
  <v-chip
    @click="select"
    class="rounded-0 mx-0 my-0"
    :outlined="!is_selected"
    :color="is_selected ? 'primary' : 'grey'"
    >{{ label.toString() || "無標籤" }}</v-chip
  >
</template>

<script>
import _ from "lodash";

export default {
  name: "chip_checkbox",
  props: ["value", "label"],
  data: () => ({}),
  computed: {
    is_selected () {
      return _.indexOf(this.value, this.label) != -1;
    },
  },
  methods: {
    select() {
      let now_value = _.cloneDeep(this.value);
      if (_.indexOf(now_value, this.label) == -1) {
        now_value = _.concat(now_value, this.label);
      } else {
        _.remove(now_value, (i) => i == this.label);
      }
      this.$emit("input", now_value);
    },
  },
};
</script>
