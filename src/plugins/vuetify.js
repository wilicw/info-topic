import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
          light: {
            primary: '#1B5E20',
            secondary: '#E65100',
            accent: '#8c9eff',
            error: '#b71c1c',
          },
        },
      },
});
