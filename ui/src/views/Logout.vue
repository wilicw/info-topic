<template>
  <v-card></v-card>
</template>

<script>
import api from "@/api";
export default {
  name: "Logout",
  created() {
    this.$root.$emit("logout");
    this.$router.push("/");
    api.clear_token();
  },
};
</script>
