import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Login from '../pages/Login.vue'
import Courses from '../pages/Courses.vue' // 🌟 นำเข้าไฟล์ Courses
import Mapping from '../pages/Mapping.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/courses', name: 'Courses', component: Courses }, // 🌟 เพิ่ม Route นี้
  { path: '/mapping', name: 'Mapping', component: Mapping }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router