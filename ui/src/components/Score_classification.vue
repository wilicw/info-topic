<template>
  <v-card>
    <v-form>
      <v-card-title class="font-weight-bold px-5">
        修改分數分類
        <v-spacer></v-spacer>
        <Edit_Dialog
          icon="mdi-plus"
          title="新增分類"
          description=""
          :global="false"
          :action="
            ({ description, global }) => new_classification(description, global)
          "
        />
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item v-for="c in classification" :key="c.id">
            <v-list-item-content>
              <v-list-item-title>{{
                classification_id_to_text(c.id)
              }}</v-list-item-title>
            </v-list-item-content>

            <v-list-item-icon>
              <Edit_Dialog
                icon="mdi-pencil"
                title="編輯分類"
                :description="c.description"
                :global="c.global"
                :action="
                  ({ description, global }) =>
                    edit_classification(c.id, description, global)
                "
              />
              <v-btn @click="delete_classification(c.id)" icon small>
                <v-icon small>mdi-close</v-icon>
              </v-btn>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-form>
  </v-card>
</template>

<script>
import _ from "lodash";
import api from "@/api";
import Edit_Dialog from "@/components/Edit_score_classification.vue";

export default {
  name: "Change_classification",
  props: ["classification", "fetch"],
  components: {
    Edit_Dialog,
  },
  methods: {
    classification_id_to_text(id) {
      const item = _.find(this.classification, { id: id });
      return item.description + (item.global ? "（組）" : "");
    },
    async new_classification(text, global) {
      if (text == "") return;
      await api.create_score_classification(text, global);
      this.fetch();
    },
    async edit_classification(id, text, global) {
      if (text == "") return;
      await api.update_score_classification(id, text, global);
      this.fetch();
    },
    async delete_classification(id) {
      await api.delete_score_classification(id);
      this.fetch();
    },
  },
};
</script>
