<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col cols="12" md="10">
        <v-card :flat="$vuetify.breakpoint.mobile" class="pa-5">
          <v-form>
            <v-card-title class="font-weight-bold">
              匯入學生資料
              <v-subheader>最後一行需為空行</v-subheader>
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col>
                  <v-select
                    :items="class_list"
                    v-model="selected_class"
                    label="班級"
                  ></v-select>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="year"
                    label="學生畢業年度（110、111...）"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <p class="mb-1">座號</p>
                  <p class="text--secondary mb-0">
                    已輸入 {{ calculate_num(seat_num) }} 筆
                  </p>
                  <v-textarea auto-grow v-model="seat_num"></v-textarea>
                </v-col>
                <v-col>
                  <p class="mb-1">學號</p>
                  <p class="text--secondary mb-0">
                    已輸入 {{ calculate_num(school_id) }} 筆
                  </p>
                  <v-textarea auto-grow v-model="school_id"></v-textarea>
                </v-col>
                <v-col>
                  <p class="mb-1">姓名</p>
                  <p class="text--secondary mb-0">已輸入 {{ calculate_num(name) }} 筆</p>
                  <v-textarea auto-grow v-model="name"></v-textarea>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn :disabled="!is_valid()" color="primary" @click="submit()"
                >送出</v-btn
              >
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from "@/api";
import { config } from "@/../config";

export default {
  name: "Change_weight",
  data: () => ({
    year: "",
    selected_class: "",
    class_list: ["甲班", "乙班", "綜高"],
    name: "",
    seat_num: "",
    school_id: "",
  }),
  async created() {
    document.title = `匯入學生資料 || ${config.title}`;
    if (!(await api.is_login())) this.$router.go(-1);
    if (api.get_group() != "admin") this.$router.go(-1);
  },
  methods: {
    split_line(text) {
      return text.replace(/(^[ \t]*\n)/gm, "").split("\n");
    },
    calculate_num(text) {
      return this.split_line(text).length - 1;
    },
    is_valid() {
      if (
        this.year == "" ||
        this.selected_class == "" ||
        this.calculate_num(this.name) == 0 ||
        this.calculate_num(this.seat_num) == 0 ||
        this.calculate_num(this.school_id) == 0 ||
        !(
          this.calculate_num(this.name) == this.calculate_num(this.seat_num) &&
          this.calculate_num(this.seat_num) == this.calculate_num(this.school_id)
        )
      ) {
        return false;
      } else {
        return true;
      }
    },
    async submit() {
      const name = this.split_line(this.name);
      const seat_num = this.split_line(this.seat_num);
      const school_id = this.split_line(this.school_id);
      let selected_class;
      switch (this.selected_class) {
        case "甲班":
          selected_class = "a";
          break;
        case "乙班":
          selected_class = "b";
          break;
        default:
          selected_class = "c";
          break;
      }
      try {
        await api.import_student(this.year, selected_class, name, seat_num, school_id);
        this.$store.commit("show_popup", { s: "success", msg: "匯入成功" });
      } catch (error) {
        this.$store.commit("show_popup", { s: "err", msg: "匯入失敗" });
      }
    },
  },
};
</script>
