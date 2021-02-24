<template>
  <v-row justify="center" class="mt-2">
    <v-col cols="12" lg="10" sm="10">
      <v-card class="rounded-0 mt-5 pa-10">
        <div v-if="loading">
          <v-skeleton-loader
            type="article, article, article"
          ></v-skeleton-loader>
        </div>
        <div v-else>
          <p class="headline mb-10 font-weight-medium">編輯專題</p>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="topic.uuid"
                label="編號"
                required
                disabled
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="topic.title"
                :counter="20"
                label="專題名稱"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                v-model="topic.teacher"
                :items="[topic.teacher]"
                disabled
                label="指導老師"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="topic.students"
                label="組員"
                required
                disabled
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-combobox
                v-model="topic.keywords"
                :items="topic._keywords"
                label="關鍵字（選取或直接輸入）"
                multiple
                small-chips
              ></v-combobox>
            </v-col>
            <v-col cols="12" sm="6">
              <v-combobox
                v-model="topic.videos_links"
                label="專題影片連結（選取或直接輸入）"
                multiple
                small-chips
              ></v-combobox>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="topic._class"
                :counter="20"
                label="專題類別"
                disabled
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <div class="mt-5">
            <p class="title">專題動機</p>
            <v-textarea
              filled
              auto-grow
              v-model="topic.description"
            ></v-textarea>
          </div>
          <div class="mt-3">
            <p class="title">問題與解決辦法</p>
            <v-textarea filled auto-grow v-model="topic.faqs"></v-textarea>
          </div>
          <div class="mt-3">
            <p class="title">
              封面<span class="body-1 text--secondary">（僅限 png、jpg）</span>
            </p>
            <v-file-input
              label="選擇檔案"
              accept="image/png, image/jpeg"
              :disabled="files.uploading"
              @change="cover_upload"
            ></v-file-input>
            <v-row>
              <v-col cols="12" sm="6">
                <v-hover v-if="topic.cover">
                  <template v-slot:default="{ hover }">
                    <v-card>
                      <v-img :src="topic.cover"></v-img>
                      <v-fade-transition>
                        <v-overlay v-if="hover" absolute color="red lighten-3">
                          <v-btn @click="topic.cover = null" icon large>
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                        </v-overlay>
                      </v-fade-transition>
                    </v-card>
                  </template>
                </v-hover>
              </v-col>
            </v-row>
          </div>
          <div class="mt-3">
            <p class="title">
              系統架構
              <span class="body-1 text--secondary">（僅限 png、jpg）</span>
            </p>
            <v-file-input
              label="選擇檔案"
              accept="image/png, image/jpeg"
              :disabled="files.uploading"
              @change="arch_upload"
            ></v-file-input>
            <v-row>
              <v-col
                v-for="(img, i) in topic.arch_imgs"
                :key="i"
                cols="12"
                sm="6"
              >
                <v-hover v-if="img">
                  <template v-slot:default="{ hover }">
                    <v-card>
                      <v-img :src="img"></v-img>
                      <v-fade-transition>
                        <v-overlay v-if="hover" absolute color="red lighten-3">
                          <v-btn @click="remove_arch(i)" icon>
                            <v-icon large>mdi-delete</v-icon>
                          </v-btn>
                        </v-overlay>
                      </v-fade-transition>
                    </v-card>
                  </template>
                </v-hover>
              </v-col>
            </v-row>
          </div>
          <div class="mt-3">
            <p class="title">
              成品示意圖
              <span class="body-1 text--secondary">（僅限 png、jpg）</span>
            </p>
            <v-file-input
              label="選擇檔案"
              accept="image/png, image/jpeg"
              :disabled="files.uploading"
              @change="results_upload"
            ></v-file-input>
            <v-row>
              <v-col
                v-for="(img, i) in topic.results_imgs"
                :key="i"
                cols="12"
                sm="6"
              >
                <v-hover v-if="img">
                  <template v-slot:default="{ hover }">
                    <v-card>
                      <v-img :src="img"></v-img>
                      <v-fade-transition>
                        <v-overlay v-if="hover" absolute color="red lighten-3">
                          <v-btn @click="remove_results(i)" icon>
                            <v-icon large>mdi-delete</v-icon>
                          </v-btn>
                        </v-overlay>
                      </v-fade-transition>
                    </v-card>
                  </template>
                </v-hover>
              </v-col>
            </v-row>
          </div>
          <div class="mt-3">
            <p class="title">
              組員照片
              <span class="body-1 text--secondary">（僅限 png、jpg）</span>
            </p>
            <v-file-input
              label="選擇檔案"
              accept="image/png, image/jpeg"
              :disabled="files.uploading"
              @change="members_upload"
            ></v-file-input>
            <v-row>
              <v-col
                v-for="(img, i) in topic.members_imgs"
                :key="i"
                cols="12"
                sm="6"
              >
                <v-hover v-if="img">
                  <template v-slot:default="{ hover }">
                    <v-card>
                      <v-img :src="img"></v-img>
                      <v-fade-transition>
                        <v-overlay v-if="hover" absolute color="red lighten-3">
                          <v-btn @click="remove_members(i)" icon>
                            <v-icon large>mdi-delete</v-icon>
                          </v-btn>
                        </v-overlay>
                      </v-fade-transition>
                    </v-card>
                  </template>
                </v-hover>
              </v-col>
            </v-row>
          </div>
          <div class="mt-3">
            <p class="title">簡報</p>
            <v-file-input
              small-chips
              label="簡報檔案（pptx, pdf, odp）"
              accept="application/vnd.openxmlformats-officedocument.presentationml.presentation, application/pdf, application/vnd.oasis.opendocu"
              show-size
              @change="upload_presentation"
            ></v-file-input>
          </div>
          <div class="mt-3">
            <p class="title">報告</p>
            <v-file-input
              small-chips
              label="報告檔案（pdf）"
              accept="application/pdf"
              show-size
              @change="upload_report"
            ></v-file-input>
          </div>
          <div class="mt-3">
            <p class="title">程式</p>
            <v-file-input
              small-chips
              label="程式檔案（zip）"
              accept="application/zip"
              show-size
              @change="upload_program"
            ></v-file-input>
          </div>
          <v-card-actions class="mt-10">
            <v-spacer></v-spacer>
            <v-btn @click="submit" class="primary">儲存</v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import api from "@/api";

export default {
  name: "Edit",
  data: () => ({
    id: "",
    loading: true,
    files: {
      uploading: false,
      report: null,
      prestation: null,
    },
    topic: {},
  }),
  async created() {
    if (!(await api.is_login())) this.$router.go(-1);
    document.title = `編輯專題 || 大安資訊專題網`;
    const id = this.$route.params.id;
    this.id = id;
    try {
      const res = await api.get_topic(id);
      this.topic = res.data;
      this.topic._keywords = this.topic.keywords;
    } catch (err) {
      console.log(err);
      return;
    }
    this.loading = false;
  },
  methods: {
    async arch_upload(e) {
      const url = await this.update_one(e, "arch", "img");
      this.topic.arch_imgs.push(url);
    },
    async cover_upload(e) {
      this.topic.cover = await this.update_one(e, "cover", "img");
    },
    async members_upload(e) {
      const url = await this.update_one(e, "members", "img");
      this.topic.members_imgs.push(url);
    },
    async results_upload(e) {
      const url = await this.update_one(e, "result", "img");
      this.topic.results_imgs.push(url);
    },
    async upload_report(e) {
      const link = await this.update_one(e, "report", "file");
      this.topic.report_file = link;
    },
    async upload_presentation(e) {
      const link = await this.update_one(e, "presentation", "file");
      this.topic.presentation_file = link;
    },
    async upload_program(e) {
      const link = await this.update_one(e, "program", "file");
      this.topic.program_file = link;
    },
    remove_results(i) {
      this.topic.results_imgs.splice(i, 1);
    },
    remove_arch(i) {
      this.topic.arch_imgs.splice(i, 1);
    },
    remove_members(i) {
      this.topic.members_imgs.splice(i, 1);
    },
    async update_one(e, tag, type) {
      const file = e;
      if (file == null || file == undefined) {
        return;
      }
      this.files.uploading = true;
      const title = `${this.topic.uuid}-${tag}--`;
      let return_url;
      switch (type) {
        case "img":
          return_url = await this.upload_image_to_server(title, file);
          break;
        case "file":
          return_url = await this.upload_file_to_server(title, file);
          break;
        default:
          break;
      }
      this.files.uploading = false;
      return return_url;
    },
    async upload_image_to_server(title, file) {
      let formData = new FormData();
      formData.append("image", file);
      formData.append("title", title);
      const res = await api.upload_image(formData);
      return res.data.link;
    },
    async upload_file_to_server(title, file) {
      let formData = new FormData();
      formData.append("file", file);
      formData.append("title", title);
      const res = await api.upload_file(formData);
      return res.data.link;
    },
    async submit() {
      const res = await api.set_topic(this.id, this.topic);
      console.log(res.data);
    },
  },
};
</script>
