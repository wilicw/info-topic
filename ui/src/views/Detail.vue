<template>
  <v-row justify="center" class="mt-3">
    <v-col cols="12" lg="8" sm="10">
      <v-card class="rounded-0 mt-5 pa-3">
        <div v-if="loading">
          <v-skeleton-loader
            type="card, avatar, article, article"
          ></v-skeleton-loader>
        </div>
        <div v-else>
          <div class="ml-5">
            <p class="title mt-5 mb-0 ml-1">{{ topic.year }} 級畢業專題</p>
            <p class="display-2 mt-3 mb-3 font-weight-bold">
              {{ topic.title }}
            </p>

            <div v-if="topic.keywords">
              <v-chip
                v-for="keyword in topic.keywords"
                :key="keyword"
                class="mt-3 mr-5 mb-5 rounded-0 font-weight-regular pa-3"
                outlined
                color="primary"
                @click="$router.push(`/keyword/${keyword}`)"
                >{{ keyword }}</v-chip
              >
            </div>

            <v-btn
              v-if="topic.presentation_file"
              @click="download(topic.presentation_file)"
              plain
              class="font-weight-bold"
            >
              <v-icon small class="mr-3">mdi-download</v-icon> 簡報
            </v-btn>

            <v-btn
              v-if="topic.report_file"
              @click="download(topic.report_file)"
              plain
              class="font-weight-bold"
            >
              <v-icon small class="mr-3">mdi-download</v-icon> 報告
            </v-btn>

            <v-btn
              v-if="topic.program_file"
              @click="download(topic.program_file)"
              plain
              class="font-weight-bold"
            >
              <v-icon small class="mr-3">mdi-download</v-icon> 程式
            </v-btn>
          </div>
          <v-img
            v-if="topic.cover"
            :src="topic.cover"
            class="ma-5"
            :class="$vuetify.breakpoint.mobile ? 'mx-0' : ''"
          ></v-img>
          <v-row>
            <v-col
              cols="12"
              sm="5"
              class="pt-5 pl-10"
              :class="$vuetify.breakpoint.mobile ? 'pa-3' : 'pa-8'"
            >
              <v-card flat class="grey--text">
                <v-divider class="my-3"></v-divider>
                編號
                <v-icon color="primary">mdi-slash-forward</v-icon>
                <span class="black--text font-weight-medium text-uppercase">
                  {{ topic.uuid }}
                </span>
                <v-divider class="my-3"></v-divider>
                指導老師
                <v-icon color="primary">mdi-slash-forward</v-icon>
                <span
                  @click="$router.push(`/teachers/${topic.teacher}`)"
                  class="black--text font-weight-medium hover"
                >
                  {{ topic.teacher }}
                </span>
                <v-divider class="my-3"></v-divider>
                組員
                <v-icon color="primary">mdi-slash-forward</v-icon>
                <span class="black--text font-weight-medium"
                  >{{ topic.students.join("、") }}
                </span>
                <v-divider class="my-3"></v-divider>
                關鍵字
                <v-icon color="primary">mdi-slash-forward</v-icon>
                <span
                  class="black--text font-weight-medium"
                  v-if="topic.keywords.length"
                  >{{ topic.keywords.join("、") }}
                </span>
                <span class="black--text font-weight-medium" v-else>無 </span>
                <v-divider class="my-3"></v-divider>
                年度
                <v-icon color="primary">mdi-slash-forward</v-icon>
                <span class="black--text font-weight-medium"
                  >{{ topic.year }}
                </span>
                <v-divider class="my-3"></v-divider>
                成績
                <v-icon color="primary">mdi-slash-forward</v-icon>
                <span class="black--text font-weight-medium"
                  >{{ topic.score }}
                </span>
                <v-divider class="my-3"></v-divider>
              </v-card>
            </v-col>
            <v-col
              cols="12"
              sm="7"
              :class="$vuetify.breakpoint.mobile ? 'pa-5' : 'pa-8'"
            >
              <p class="display-1 font-weight-medium">
                <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 動機
              </p>
              <p class="content" v-if="topic.description">
                {{ topic.description }}
              </p>
              <p class="content" v-else>無資料</p>
            </v-col>
          </v-row>
          <div :class="$vuetify.breakpoint.mobile ? 'pa-0' : 'pa-8'">
            <div class="py-5" v-if="topic.faqs">
              <p class="display-1 font-weight-medium">
                <v-icon class="mb-1" color="primary">mdi-pound</v-icon>
                問題與解決辦法
              </p>
              <p class="py-5 content">{{ topic.faqs }}</p>
            </div>
            <div class="py-5" v-if="topic.arch_imgs.length">
              <p class="display-1 font-weight-medium">
                <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 系統架構
              </p>
              <v-row class="pa-5">
                <v-col
                  cols="12"
                  :sm="topic.arch_imgs.length == 1 ? 12 : 6"
                  v-for="img in topic.arch_imgs"
                  :key="img"
                >
                  <v-img :src="img"></v-img
                ></v-col>
              </v-row>
            </div>
            <div class="py-5" v-if="topic.results_imgs.length">
              <p class="display-1 font-weight-medium">
                <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 成品
              </p>
              <v-row class="pa-5">
                <v-col
                  cols="12"
                  :sm="topic.results_imgs.length == 1 ? 12 : 6"
                  v-for="img in topic.results_imgs"
                  :key="img"
                >
                  <v-img :src="img"></v-img
                ></v-col>
              </v-row>
            </div>
            <div class="py-5" v-if="topic.members_imgs.length">
              <p class="display-1 font-weight-medium">
                <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 組員照片
              </p>
              <v-row class="pa-5">
                <v-col
                  cols="12"
                  :sm="topic.members_imgs.length == 1 ? 12 : 6"
                  v-for="img in topic.members_imgs"
                  :key="img"
                >
                  <v-img :src="img"></v-img
                ></v-col>
              </v-row>
            </div>
            <div class="py-5" v-if="topic.videos_links.length">
              <p class="display-1 font-weight-medium">
                <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 影片
              </p>
              <v-card flat min-height="800">
                <iframe
                  v-for="id in topic.videos_links"
                  :key="id"
                  style="height: 100%; width: 100%; position: absolute"
                  :src="`https://www.youtube.com/embed/${id}`"
                  frameborder="0"
                  allowfullscreen
                ></iframe>
              </v-card>
            </div>
          </div>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import api from "@/api";

export default {
  name: "Detail",
  data: () => ({
    loading: true,
    topic: {
      id: 0,
      uuid: "",
      title: "",
      year: "",
      description: "",
      cover: "",
      keywords: [],
      students: [],
      teacher: "",
      faqs: "",
      report_file: "",
      presentation_file: "",
      program_file: "",
      videos_links: [],
      arch_imgs: [],
      members_imgs: [],
      results_imgs: [],
    },
  }),
  async created() {
    const uuid = this.$route.params.uuid;
    try {
      const res = await api.get_topic(uuid);
      this.topic = res.data;
      document.title = `${this.topic.title} || 大安資訊專題網`;
    } catch (err) {
      console.log(err);
      return;
    }
    this.loading = false;
  },
  methods: {
    download(link) {
      window.open(link, "_blank");
    },
  },
};
</script>
