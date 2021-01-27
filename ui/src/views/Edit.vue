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
              <v-hover v-if="topic.cover_photo_link">
                <template v-slot:default="{ hover }">
                  <v-card>
                    <v-img :src="topic.cover_photo_link"></v-img>
                    <v-fade-transition>
                      <v-overlay v-if="hover" absolute color="red lighten-3">
                        <v-btn
                          @click="topic.cover_photo_link = null"
                          icon
                          large
                        >
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
              v-for="(img, i) in topic.arch_photo_links"
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
              v-for="(img, i) in topic.result_photo_links"
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
              v-for="(img, i) in topic.members_photo_links"
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
const axios = require("axios");

export default {
  name: "Edit",
  data: () => ({
    teachers_list: ["王敏男"],
    files: {
      uploading: false,
      report: null,
      prestation: null,
    },
    topic: {
      id: 0,
      uuid: "G110B02",
      score: 4,
      year: 110,
      name: "成績單掃喵器",
      keywords: ["影像處理", "神經網路", "OCR"],
      _keywords: ["影像處理", "神經網路", "OCR"],
      _class: "",
      teacher: "王敏男",
      report_link: "",
      members: ["卓于傑", "林士傑", "張庭瑋", "張裕偉", "郭少禾"],
      cover_photo_link:
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data1.png",
      motivation:
        "學校的期末成績處理作業往往是先藉由人工的方式將紙本成績單上的成績輸入至Microsoft Excel等試算表軟體，再透過電子檔進行各式操作。而輸入的過程往往會因為作業者粗心而發生失誤，所以我們希望搭配手機的拍照功能，並結合影像處理、神經網路、OCR等技術，開發一款能夠掃描紙本成績單，將成績單上的數字進行辨識，然後自動轉成試算表電子檔的手機應用程式，以協助此一作業的進行，達到縮減作業時間、減少人工導致之失誤的目的。",
      FAQs:
        "Q0、在抓取成績單定位點時準確度不佳：在將影像二值化後，定位點會發生破洞的情況，造成回字形定位點無法偵測。\n A0、而我們發現可以透過高斯模糊將破口補齊，進而正確判斷位置。方形破洞透過高斯模糊後可被 OpenCV 的cv2. findContours 正確偵測。\n\n Q1、圖片由應用程式擷取送出後，伺服器端無法正常處理\nA1、因為在手機端程式抓取預覽式縮圖，造成上傳至 Web API 時，OpenCV 圖片縮放回正常大小，導致成績單內容全數失真，因而無法正常辨識以及處理。所以改寫 APP 讓圖片先暫存至手機儲存空間，再將圖片轉碼上傳至 Web API，方可正常辨識以及處理。 \n\nQ2、手寫數字辨識度不佳 \nA2、在使用網路上的神經網路模型後，發現辨識率低於 50%，成效不佳，所以我們決定採用 Keras 來自己建構神經網路，經過測試之後發現辨識率依舊低迷，所以對資料集進行資料加強。而經過資料增強後，除了數字 1 以外，發現其他的數字的辨識率都有明顯提升。檢視程式碼之後發現，擷取數字後，是將影像直接放大為 28x28 這樣會使數字 1 被拉寬成一塊長方形，導致無法辨識出數字 1。而我們改為等比例放大數字，使辨識率有所提升。 \n\nQ3、Python 環境架設失敗\n A3、一開始我們使用 Microsoft Windows 架設 Python 伺服器環境時，遇到 Keras 安裝失敗、套件與系統產生衝突。因 Microsoft Windows 環境架設問題多，我們決定使用更加穩定與開放的 Linux 系統進行伺服器架設。",
      members_photo_links: [
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data4.jpg",
      ],
      arch_photo_links: [
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data5.png",
      ],
      result_photo_links: [
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data6.png",
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data7.png",
      ],
      videos_link: ["R4TL00kru88"],
    },
  }),
  methods: {
    async arch_upload(e) {
      const url = await this.update_one(e, "系統架構");
      this.topic.arch_photo_links.push(url);
    },
    async cover_upload(e) {
      this.topic.cover_photo_link = await this.update_one(e, "封面");
    },
    async members_upload(e) {
      const url = await this.update_one(e, "組員");
      this.topic.members_photo_links.push(url);
    },
    async results_upload(e) {
      const url = await this.update_one(e, "成品");
      this.topic.result_photo_links.push(url);
    },
    remove_results(i) {
      this.topic.result_photo_links.splice(i, 1);
    },
    remove_arch(i) {
      this.topic.arch_photo_links.splice(i, 1);
    },
    remove_members(i) {
      this.topic.members_photo_links.splice(i, 1);
    },
    async update_one(e, tag) {
      const file = e;
      if (file == null || file == undefined) {
        return;
      }
      this.files.uploading = true;
      const title = `${this.topic.uuid} ${this.topic.name} ${tag}`;
      let return_url = await this.upload_image_to_imgur(title, file);
      this.files.uploading = false;
      return return_url;
    },
    async upload_image_to_imgur(title, file) {
      const imgur_client_id = "e41ec52ccc51322";
      let formData = new FormData();
      formData.append("image", file);
      formData.append("title", title);
      const res = await axios({
        method: "POST",
        url: "https://api.imgur.com/3/image",
        data: formData,
        headers: {
          Authorization: "Client-ID " + imgur_client_id,
        },
        mimeType: "multipart/form-data",
      });
      return res.data.data.link;
    },
    submit() {
      console.log(this.topic);
    },
  },
};
</script>
