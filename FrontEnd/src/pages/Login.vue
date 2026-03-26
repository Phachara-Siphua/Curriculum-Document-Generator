<template>
  <div class="login-wrapper">
    <div class="card login-card">
      <div class="card-header">🚪 กรุณาป้อน ICIT Account และรหัสผ่าน</div>
      <div class="card-body">
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>ICIT Account</label>
            <input v-model="username" type="text" required>
          </div>
          <div class="form-group">
            <label>รหัสผ่าน</label>
            <input v-model="password" type="password" required>
          </div>
          <button type="submit" class="btn-primary" :disabled="isLoading">
            {{ isLoading ? 'กำลังตรวจสอบ...' : 'เข้าสู่ระบบ' }}
          </button>
          <div v-if="message" :class="['alert', status]">{{ message }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../store' // 🌟 นำเข้า Store

const router = useRouter()
const username = ref('')
const password = ref('')
const message = ref('')
const status = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  try {
    const response = await fetch('http://127.0.0.1:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    const data = await response.json()

    if (data.status === 'success') {
      authStore.login(data.user_data) // 🌟 บันทึกสถานะล็อกอิน
      router.push('/courses') // 🌟 ล็อกอินเสร็จให้เด้งไปหน้า ข้อมูลหลักสูตร
    } else {
      message.value = `❌ ${data.message}`
      status.value = 'error'
    }
  } catch (error) {
    message.value = '❌ เชื่อมต่อ Backend ไม่ได้'
    status.value = 'error'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-wrapper { display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #e0e0e0;}
.card { background-color: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); overflow: hidden; max-width: 500px; width: 100%;}
.card-header { background-color: #e85d22; color: white; padding: 15px; font-weight: bold; }
.card-body { padding: 20px; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px;}
.form-group input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.btn-primary { width: 100%; background-color: #e85d22; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-size: 16px; }
.btn-primary:hover { background-color: #d14d18; }
.alert { margin-top: 15px; padding: 10px; border-radius: 4px; font-size: 14px; }
.error { background-color: #f8d7da; color: #721c24; }
</style>