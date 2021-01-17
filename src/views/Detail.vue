<template>
  <v-row justify="center" class="mt-5">
    <v-col cols="12" lg="8" sm="10">
      <v-card flat class="rounded-0 mt-5">
        <div class="ml-5">
          <p class="title mt-5 mb-0 ml-1">{{ topic.year }} 級畢業專題</p>
          <p class="display-2 mt-1 mb-2 font-weight-bold">{{ topic.name }}</p>
          <v-chip
            v-for="keyword in topic.keywords"
            :key="keyword"
            class="mt-1 ml-2 mr-3 rounded-0 font-weight-bold"
            label
            small
            dark
            >{{ keyword }}</v-chip
          >
        </div>
        <br />
        <v-img :src="topic.cover_photo_link" class="ma-5"></v-img>
        <v-row>
          <v-col cols="12" sm="5" class="pt-5 pa-5 pl-10">
            <v-card flat class="grey--text">
              <v-divider class="my-3"></v-divider>
              編號
              <v-icon color="primary">mdi-slash-forward</v-icon>
              <span class="black--text font-weight-medium">
                {{ topic.uuid }}
              </span>
              <v-divider class="my-3"></v-divider>
              指導老師
              <v-icon color="primary">mdi-slash-forward</v-icon>
              <span class="black--text font-weight-medium">
                {{ topic.teacher }}
              </span>
              <v-divider class="my-3"></v-divider>
              組員
              <v-icon color="primary">mdi-slash-forward</v-icon>
              <span class="black--text font-weight-medium"
                >{{ topic.members.join("、") }}
              </span>
              <v-divider class="my-3"></v-divider>
              關鍵字
              <v-icon color="primary">mdi-slash-forward</v-icon>
              <span class="black--text font-weight-medium"
                >{{ topic.keywords.join("、") }}
              </span>
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
          <v-col cols="12" sm="7" class="pa-10">
            <p class="display-1 font-weight-medium">
              <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 動機
            </p>
            <p>{{ topic.motivation }}</p>
          </v-col>
        </v-row>
        <div class="pa-10 px-5">
          <p class="display-1 font-weight-medium">
            <v-icon class="mb-1" color="primary">mdi-pound</v-icon>
            問題與解決辦法
          </p>
          <p class="pa-5">{{ topic.FAQs }}</p>
        </div>
        <div class="pa-10 px-5">
          <p class="display-1 font-weight-medium">
            <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 系統架構
          </p>
          <v-img class="pa-5" :src="topic.arch_photo_link"></v-img>
        </div>
        <div class="pa-10 px-5">
          <p class="display-1 font-weight-medium">
            <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 成品
          </p>
          <v-row class="pa-5">
            <v-col cols="6" v-for="img in topic.result_photo_links" :key="img">
              <v-img :src="img"></v-img
            ></v-col>
          </v-row>
        </div>
        <div class="pa-10 px-5">
          <p class="display-1 font-weight-medium">
            <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 組員照片
          </p>
          <v-img class="pa-5" :src="topic.members_photo_link"></v-img>
        </div>
        <div class="pa-10 px-5">
          <p class="display-1 font-weight-medium">
            <v-icon class="mb-1" color="primary">mdi-pound</v-icon> 影片
          </p>
          <v-card flat min-height="800">
            <iframe
              v-for="id in topic.videos_link"
              :key="id"
              style="height: 100%; width: 100%; position: absolute"
              :src="'//www.youtube.com/embed/' + id"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </v-card>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "Detail",
  data: () => ({
    topic: {
      id: 0,
      uuid: "G110B02",
      score: 4,
      year: 110,
      name: "成績單掃喵器",
      keywords: ["影像處理", "神經網路", "OCR"],
      teacher: "王敏男",
      report_link: "",
      members: ["卓于傑", "林士傑", "張庭瑋", "張裕偉", "郭少禾"],
      cover_photo_link:
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data1.png",
      motivation:
        "學校的期末成績處理作業往往是先藉由人工的方式將紙本成績單上的成績輸入至Microsoft Excel等試算表軟體，再透過電子檔進行各式操作。而輸入的過程往往會因為作業者粗心而發生失誤，所以我們希望搭配手機的拍照功能，並結合影像處理、神經網路、OCR等技術，開發一款能夠掃描紙本成績單，將成績單上的數字進行辨識，然後自動轉成試算表電子檔的手機應用程式，以協助此一作業的進行，達到縮減作業時間、減少人工導致之失誤的目的。",
      FAQs:
        "Q0、在抓取成績單定位點時準確度不佳：在將影像二值化後，定位點會發生破洞的情況，造成回字形定位點無法偵測。 A0、而我們發現可以透過高斯模糊將破口補齊，進而正確判斷位置。方形破洞透過高斯模糊後可被 OpenCV 的cv2. findContours 正確偵測。 Q1、圖片由應用程式擷取送出後，伺服器端無法正常處理A1、因為在手機端程式抓取預覽式縮圖，造成上傳至 Web API 時，OpenCV 圖片縮放回正常大小，導致成績單內容全數失真，因而無法正常辨識以及處理。所以改寫 APP 讓圖片先暫存至手機儲存空間，再將圖片轉碼上傳至 Web API，方可正常辨識以及處理。 Q2、手寫數字辨識度不佳 A2、在使用網路上的神經網路模型後，發現辨識率低於 50%，成效不佳，所以我們決定採用 Keras 來自己建構神經網路，經過測試之後發現辨識率依舊低迷，所以對資料集進行資料加強。而經過資料增強後，除了數字 1 以外，發現其他的數字的辨識率都有明顯提升。檢視程式碼之後發現，擷取數字後，是將影像直接放大為 28x28 這樣會使數字 1 被拉寬成一塊長方形，導致無法辨識出數字 1。而我們改為等比例放大數字，使辨識率有所提升。 Q3、Python 環境架設失敗 A3、一開始我們使用 Microsoft Windows 架設 Python 伺服器環境時，遇到 Keras 安裝失敗、套件與系統產生衝突。因 Microsoft Windows 環境架設問題多，我們決定使用更加穩定與開放的 Linux 系統進行伺服器架設。",
      members_photo_link:
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data4.jpg",
      arch_photo_link:
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data5.png",
      result_photo_links: [
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data6.png",
        "http://info.taivs.tp.edu.tw/topic/upload/110/G110B02/G110B02_Data7.png",
      ],
      videos_link: ["R4TL00kru88"],
    },
  }),
};
</script>
