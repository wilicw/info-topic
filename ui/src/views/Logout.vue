<template>
  <v-card></v-card>
</template>

<script>
export default {
  name: "Logout",
  created() {
    this.$root.$emit("logout");
    this.$router.push("/");
  },
};
</script>
