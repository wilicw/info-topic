<template>
  <v-container>
    <br /><v-row justify="center" class="mt-5">
      <v-col cols="12" md="4">
        <v-card color="transparent" flat>
          <v-card-title>
            <div class="display-3 mt-5">
              找不到此頁 <br />
              404 Error
            </div>
          </v-card-title>
          <v-card-text>
            <div class="grey--text lighten-5">
              The page you are trying to get to never existed in this reality,
              or has migrated to a parallel universe.
            </div>
            <div class="my-2">
              <br />Try going back to home page and repeating your action. Or,
              contact helpdesk for support.
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="$router.push('/year/latest')">
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
  created() {
    document.title = `找不到此頁 || ${config.title}`;
  },
};
</script>
