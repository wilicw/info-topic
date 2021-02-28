<template>
  <div>
    <v-snackbar
      v-model="trigger"
      timeout="2000"
      :color="err ? 'pink' : 'success'"
    >
      {{ msg }}
    </v-snackbar>
  </div>
</template>

<script>
export default {
  name: "Popup",
  data: () => ({
    trigger: false,
    err: false,
    success: false,
  }),
  watch: {
    "$store.state.popup.state": function () {
      this.err = this.$store.state.popup.state == "err";
      this.success = this.$store.state.popup.state == "success";
      this.trigger = this.err || this.success;
    },
    trigger: function () {
      this.init();
    },
  },
  methods: {
    init() {
      if (!this.err && !this.success)
        this.$store.commit("show_popup", { s: "none", msg: "" });
    },
  },
  computed: {
    msg: function () {
      return this.$store.state.popup.msg;
    },
  },
};
</script>