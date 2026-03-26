<template>
  <header class="topbar-container">
    <div class="topbar">
      <div class="breadcrumb">ระบบจัดการโครงสร้างหลักสูตร</div>
      <div class="actions">
        <button v-if="!authStore.isLoggedIn" class="login-btn-orange" @click="$router.push('/login')">เข้าสู่ระบบ</button>
        
        <div v-else class="user-menu">
          <span class="user-icon">👤 {{ authStore.user?.name }}</span>
          <button class="logout-btn" @click="handleLogout">ออกจากระบบ</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { authStore } from '../store'

const router = useRouter()
const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
/* เอาสไตล์เดิมมา แล้วเพิ่ม CSS ด้านล่างนี้ต่อท้ายครับ */
.topbar-container { padding: 15px 15px 10px 15px; }
.topbar { background-color: white; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.breadcrumb { font-weight: normal; color: #000; font-size: 16px; }
.login-btn-orange { background-color: #e36c3e; color: white; border: none; padding: 8px 20px; border-radius: 6px; cursor: pointer; font-size: 15px;}
.user-menu { display: flex; align-items: center; gap: 15px; font-weight: bold; color: #e36c3e;}
.logout-btn { background: none; border: 1px solid #ccc; padding: 4px 10px; border-radius: 4px; cursor: pointer;}
.logout-btn:hover { background-color: #fee; color: red;}
</style>