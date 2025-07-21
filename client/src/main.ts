import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import { vuetify } from './vuetify'
import './assets/style.css'
import '@mdi/font/css/materialdesignicons.css'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)
app.use(pinia)
app.use(vuetify)
app.use(router)
app.mount('#app')
