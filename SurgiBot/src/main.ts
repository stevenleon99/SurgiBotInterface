import { createApp } from "vue";
import "./styles.css";
import App from "./App.vue";

// Vuetify
// https://vuetifyjs.com/en/getting-started/installation/#existing-projects
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import store from './store/store.js'

const vuetify = createVuetify({
    components,
    directives,
    icons: {
      defaultSet: 'mdi',
      aliases,
      sets: {
        mdi,
      },
    },
  })

const app = createApp(App);
app.use(vuetify);
app.use(store);
app.mount("#app");

