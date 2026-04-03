<template>
  <div class="login-container">
    <div class="login-box">
      <img src="/img/logo.png" alt="Logo" class="login-logo" />
      <h2>เข้าสู่ระบบ</h2>
      <p>ระบบจัดการหลักสูตร (Rewrite)</p>
      
      <form @submit.prevent="handleLogin">
        <input v-model="username" type="text" placeholder="Username" required class="input-field">
        <input v-model="password" type="password" placeholder="Password" required class="input-field">
        <button type="submit" class="btn-login" :disabled="isLoading">
          {{ isLoading ? 'กำลังตรวจสอบ...' : 'เข้าสู่ระบบ' }}
        </button>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCookie } from '#app'

// ปิด Layout ปกติ (ไม่ให้โชว์ Sidebar ในหน้า Login)
definePageMeta({ layout: false })

const router = useRouter()
const userCookie = useCookie('user_data') // สร้างตัวแปรเก็บลง Cookie
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    // ยิง API ไปหา FastAPI
    const response = await $fetch('http://127.0.0.1:8000/api/login', {
      method: 'POST',
      body: { username: username.value, password: password.value }
    })

    if (response.status === 'success') {
      userCookie.value = response.user_data // บันทึกข้อมูลลง Cookie
      router.push('/') // เด้งไปหน้า แผงควบคุม
    } else {
      errorMessage.value = response.message
    }
  } catch (error) {
    errorMessage.value = 'ไม่สามารถเชื่อมต่อ Backend ได้'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container { display: flex; justify-content: center; align-items: center; height: 100vh; background: #2c3e50; }
.login-box { background: white; padding: 40px; border-radius: 8px; width: 350px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.input-field { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
.btn-login { width: 100%; padding: 12px; background: #e67e22; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; }
.btn-login:hover { background: #d35400; }
.error-text { color: red; margin-top: 10px; }
/* 🌟 จัดขนาดและระยะห่างของโลโก้หน้า Login */
.login-logo {
  width: 200px; /* ปรับขนาดความกว้างได้ตามต้องการ */
  height: auto;
  margin-bottom: 15px;
  }
</style>