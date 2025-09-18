import "@mdi/font/css/materialdesignicons.css";

import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue";

import App from "./App.vue";
import "./assets/style.css";
import router from "./router";
import { vuetify } from "./vuetify";

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App);
app.use(pinia);
app.use(vuetify);
app.use(router);
app.mount("#app");
