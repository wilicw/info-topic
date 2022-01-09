<template>
  <v-container>
    <br /><v-row justify="center" class="mt-5">
      <v-col cols="12" :md="gif ? 6 : 4">
        <v-card color="transparent" flat>
          <v-card-title>
            <div class="display-3 mt-5">
              找不到此頁 <br />
              404 Error
            </div>
          </v-card-title>
          <v-card-text v-if="!gif">
            <div class="grey--text lighten-5">
              The page you are trying to get to never existed in this reality, or has
              migrated to a parallel universe.
            </div>
            <div class="my-2">
              <br />Try going back to home page and repeating your action. Or, contact
              helpdesk for support.
            </div>
          </v-card-text>
          <v-card-text v-else>
            <v-img
              class="mx-auto mt-5"
              src="http://thecatapi.com/api/images/get?format=src&type=gif"
            ></v-img>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" class="mx-auto" @click="$router.push('/year/latest')">
              瀏覽專題
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { config } from "@/../config";

export default {
  name: "NotFound",
  data: () => ({
    gif: false,
  }),
  created() {
    const self = this;
    document.title = `找不到此頁 || ${config.title}`;
    setTimeout(function () {
      self.gif = true;
    }, 2000);
  },
};
</script>
