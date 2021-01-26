<template>
  <v-row justify="center" class="mt-2">
    <v-col cols="12" lg="10" sm="10">
      <v-card class="rounded-0 mt-5 pa-10">
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
              v-model="topic.name"
              :counter="20"
              label="專題名稱"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              v-model="topic.teacher"
              :items="teachers_list"
              disabled
              label="指導老師"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="topic.members"
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
              v-model="topic.videos_link"
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
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <div class="mt-5">
          <p class="title">專題動機</p>
          <v-textarea filled auto-grow v-model="topic.motivation"></v-textarea>
        </div>
        <div class="mt-3">
          <p class="title">問題與解決辦法</p>
          <v-textarea filled auto-grow v-model="topic.FAQs"></v-textarea>
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
              <v-hover v-if="files.cover">
                <template v-slot:default="{ hover }">
                  <v-card>
                    <v-img :src="files.cover"></v-img>
                    <v-fade-transition>
                      <v-overlay v-if="hover" absolute color="red lighten-3">
                        <v-btn @click="files.arch = null" icon large>
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
            <v-col cols="12" sm="6">
              <v-hover v-if="files.arch">
                <template v-slot:default="{ hover }">
                  <v-card>
                    <v-img :src="files.arch"></v-img>
                    <v-fade-transition>
                      <v-overlay v-if="hover" absolute color="red lighten-3">
                        <v-btn @click="files.arch = null" icon>
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
            <v-col v-for="(img, i) in files.results" :key="i" cols="12" sm="6">
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
            <v-col cols="12" sm="6">
              <v-hover v-if="files.members">
                <template v-slot:default="{ hover }">
                  <v-card>
                    <v-img :src="files.members"></v-img>
                    <v-fade-transition>
                      <v-overlay v-if="hover" absolute color="red lighten-3">
                        <v-btn @click="files.members = null" icon>
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
          ></v-file-input>
        </div>
        <div class="mt-3">
          <p class="title">報告</p>
          <v-file-input
            small-chips
            label="報告檔案（pdf）"
            accept="application/pdf"
            show-size
          ></v-file-input>
        </div>
        <v-card-actions class="mt-10">
          <v-spacer></v-spacer>
          <v-btn @click="submit" class="primary">儲存</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "Edit",
  data: () => ({
    password: "",
  }),
  methods: {
    submit() {},
  },
};
</script>
