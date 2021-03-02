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
  }),
  watch: {
    success: function () {
      this.trigger = this.err || this.success;
    },
    err: function () {
      this.trigger = this.err || this.success;
    },
    trigger: function () {
      this.init();
    },
  },
  methods: {
    init() {
      if (!this.trigger)
        this.$store.commit("show_popup", { s: "none", msg: "" });
    },
  },
  computed: {
    msg: function () {
      return this.$store.state.popup.msg;
    },
    err: function () {
      return this.$store.state.popup.state == "err";
    },
    success: function () {
      return this.$store.state.popup.state == "success";
    },
  },
};
</script>
