<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-col v-for="t in teachers" :key="t.name" cols="6" xs="12">
        <v-card class="rounded-0 pa-5">
          <v-card-title class="headline font-weight-bold">
            {{ t.name }} <span class="title">老師</span>
          </v-card-title>
          <v-card-text>
            {{ t.major }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn plain>瀏覽曾經專題內容</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Teachers",
  data: () => ({
    teachers: [
      {
        name: "黃紹緯",
        major: "晶片控制與 IoT 應用",
      },
      {
        name: "徐慶堂",
        major: "物聯網應用",
      },

      {
        name: "王敏男",
        major: "樂高及晶片控制",
      },

      {
        name: "黃博原",
        major: "感測器應用",
      },

      {
        name: "沈彥良",
        major: "爬蟲程式設計",
      },

      {
        name: "張佩琪",
        major: "晶片控制與 Unity 應用",
      },
    ],
  }),
  methods: {},
};
</script>
