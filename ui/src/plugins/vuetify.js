import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#5A7D7C',
        secondary: '#232C33',
        accent: '#8c9eff',
        error: '#b71c1c',
        background: '#fbfdfc'
      },
      dark: {
        primary: '#71a3a2',
        secondary: '#fcfcfc',
        accent: '#8c9eff',
        error: '#db4444',
        background: '#141413'
      },
    },
  },
});
