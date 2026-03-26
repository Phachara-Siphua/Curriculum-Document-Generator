

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // นำเข้า router

const app = createApp(App)
app.use(router) // สั่งให้ Vue ใช้งาน Router
app.mount('#app')
