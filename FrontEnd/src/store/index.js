// src/store/index.js
import { reactive } from 'vue'

export const authStore = reactive({
  isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
  user: JSON.parse(localStorage.getItem('user')) || null,
  
  login(userData) {
    this.isLoggedIn = true
    this.user = userData
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('user', JSON.stringify(userData))
  },
  logout() {
    this.isLoggedIn = false
    this.user = null
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('user')
  }
})