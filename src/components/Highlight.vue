<template>
  <v-container>
    <v-btn
      class="next_btn float_btn"
      v-if="!$vuetify.breakpoint.mobile"
      icon
      fab
      small
      absolute
      top
      right
      @click="next_topic()"
    >
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>

    <v-btn
      class="pre_btn float_btn"
      v-if="!$vuetify.breakpoint.mobile"
      icon
      fab
      small
      absolute
      top
      left
      @click="pre_topic()"
    >
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>
    <v-row
      align="center"
      justify="center"
      class="mt-5"
      style="min-height: 80vh"
    >
      <v-col cols="10" md="5" class="mx-10">
        <p class="subtitle-1 mb-5 ml-1">{{ topic.year }} 級專題製作</p>
        <h1 class="display-3 font-weight-bold mb-7">
          {{ topic.title }}
        </h1>
        <p class="subheading font-weight-regular">
          {{ text_truncate(topic.description) }}
        </p>
        <span class="grey--text hover">檢視完整專題</span>
      </v-col>
      <v-col
        cols="12"
        md="5"
        class="mx-10"
        :order="$vuetify.breakpoint.mobile ? 'first' : 'last'"
      >
        <v-img
          transition="scale-transition"
          :alt="topic.title"
          contain
          :src="topic.cover"
          class="cover"
          :max-height="$vuetify.breakpoint.mobile ? '20em' : '45em'"
          v-touch="{
            left: () => next_topic(),
            right: () => pre_topic(),
          }"
        />
      </v-col>
    </v-row>
    <div style="text-align: right" class="floating mx-0">
      <span
        class="mt-3 hover body-2 grey--text"
        @click="$vuetify.goTo('#all_topics')"
      >
        更多專題 <v-icon>mdi-chevron-double-down</v-icon>
      </span>
    </div>
  </v-container>
</template>

<script>
import _ from "lodash";
export default {
  name: "Highlight",
  data: () => ({
    max_text_turncate: 130,
    highlight_topics_id: 0,
    topic: {},
    highlight_topics: [
      {
        title: "零接觸取貨機",
        cover:
          "http://info.taivs.tp.edu.tw/topic/upload/110/G110B09/G110B09_Data1.png",
        year: 110,
        description:
          "疫情至今尚未緩解，他帶給人們在生活中無數的不便，人們的生活習慣也被迫做出許多改變。人與人間的接觸是感染的最大風險，人們為了減少接觸必會避免外出，轉而選擇網購等方式來採買日常生活用品，而網購在取貨的過程，不管是超商取貨或是郵寄，都不乏會與超商店員或外送員接觸，而現今的郵局的i郵箱是使用觸控螢幕來完成操作，螢幕也會有許多使用者進行操作，在此之中我們就與前一位使用者間接接觸。在需多情況下都充滿直接與間接接觸的機會，這些接觸都有可能讓病毒趁虛而入，減少接觸是勢所必然要做的事。 為了減少接觸，零接觸的商機也因此產生。我們由零接觸及生活中的購物發想，希望能藉這次專題的機會，製作出能在不需接觸機器的情況下完成取貨的機器，可以達到完全零接觸，並為防疫作出貢獻的作品，讓大家更重視零接觸的發展，使其發展更全面讓我們遏止病毒的肆虐，守護健康且不影響生活。",
      },
      {
        title: "星之彩",
        cover:
          "http://info.taivs.tp.edu.tw/topic/upload/110/G110B08/G110B08_Data1.png",
        year: 110,
        description:
          "遊戲又被稱為第九藝術，我們便想用程式碼創造屬於我們的藝術，近年來推出的優秀作品，諸如From Software的<黑暗靈魂>、Team cherry的<空洞騎士>，以及最近台灣獨立遊戲團隊玻璃心工作室的<守夜人：長夜>，都是我們所參考的對象，我們想用旁人看似冷冰冰的程式碼加上課餘興趣所學的美術，表達我們對遊戲的熱愛以及堅持。",
      },
      {
        title: "腐政",
        cover:
          "http://info.taivs.tp.edu.tw/topic/upload/109/G109C03/G109C03_Data1.png",
        year: 109,
        description:
          "我們這組希望藉著我們想做遊戲的心，大家能夠更加瞭解過去台灣的歷史大家對於二二八事件的感想頂多就是放假或只是一個過去的歷史，能透過遊戲來讓大家重新想起當年發生的事，是我們這組的目標。我們未來也想試試其他不同的風格，我們不會被同一風格所侷限，也是我們這組的風格，我們想利用製作遊戲讓大家了解這點",
      },
      {
        title: "體感高爾夫 & Motion",
        cover:
          "http://info.taivs.tp.edu.tw/topic/upload/108/G108A09/G108A09_Data1.jpg",
        year: 108,
        description:
          "在這科技發展快速的年代，遊戲已成為人們生活中不可或缺的休閒活動。我們發現市面上的遊戲皆沒有除了螢幕與聲音以外給予玩家現實生活回饋的機制，我們認為玩家遊玩遊戲的投入感可以透過在適當時間震動等方式增進。但在這遊戲開發資源充足的時代中，開發者沒有一個簡單易用的SDK (Software Development Kit)實作與用戶回饋的機制，同時市面上也沒有經濟實惠的回饋裝置。因此，我們製作了一個SDK提供開發者一個簡單易用、高擴充性的C#函式庫。為了示範及讓開發者了解其開發方法，我們決定製作一個對身體有益同時也可以玩樂的體感高爾夫球遊戲，擊球、獲勝等時刻使用SDK震動自製的Arduino裝置。",
      },
    ],
  }),
  created() {
    this.highlight_topics_id = _.random(0, this.highlight_topics.length - 1);
    this.topic = this.highlight_topics[this.highlight_topics_id];
  },
  methods: {
    next_topic() {
      const now_id = this.highlight_topics_id;
      this.highlight_topics_id =
        now_id + 1 == this.highlight_topics.length ? 0 : now_id + 1;
      this.topic = this.highlight_topics[this.highlight_topics_id];
    },
    pre_topic() {
      const now_id = this.highlight_topics_id;
      this.highlight_topics_id =
        now_id == 0 ? this.highlight_topics.length - 1 : now_id - 1;
      this.topic = this.highlight_topics[this.highlight_topics_id];
    },
    text_truncate(text) {
      if (text.length > this.max_text_turncate) {
        return text.slice(0, this.max_text_turncate) + "...";
      }
      return text;
    },
    random_rotate() {
      return `transform: rotate(${_.random(-5, 5)}deg);`;
    },
  },
};
</script>
<style scoped>
.float_btn {
  top: 45vh !important;
}

.next_btn {
  right: 3em;
}

.pre_btn {
  left: 3em;
}

.cover {
  filter: drop-shadow(0.35rem 0.35rem 0.4rem rgba(0, 0, 0, 0.5));
}

.floating {
  animation-name: floating;
  animation-duration: 2s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

@keyframes floating {
  100%,
  0% {
    transform: translate(0, 0px);
  }
  50% {
    transform: translate(0, 15px);
  }
}
</style>