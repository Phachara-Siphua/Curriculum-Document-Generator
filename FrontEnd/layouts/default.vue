<template>
  <div class="app-layout">
    <!-- Sidebar ด้านซ้าย -->
    <aside class="sidebar">      
      <div class="logo">
        <!-- 🌟 เพิ่มรูปโลโก้ตรงนี้ -->
        <img src="/img/logo.png" alt="CIT Logo" class="sidebar-logo" />
        <h2>CIT (วทอ.)</h2>
      </div>
      <nav class="menu">
        <NuxtLink to="/">🏠 แผงควบคุม</NuxtLink>
        <NuxtLink to="/courses">📄 จัดการรายวิชา & Mapping</NuxtLink>
        <!-- 🌟 เมนูใหม่ที่เพิ่งเพิ่ม -->
        <NuxtLink to="/course-descriptions">📖 คำอธิบายรายวิชา</NuxtLink>
        <NuxtLink to="/documents">🖨️ สร้างเล่มหลักสูตร</NuxtLink>
      </nav>
      <div class="logout-zone">
        <button @click="logout" class="btn-logout">ออกจากระบบ</button>
      </div>
    </aside>

    <!-- พื้นที่เนื้อหาด้านขวา -->
    <main class="main-content">
      <header class="topbar">
        <span>ระบบจัดการโครงสร้างหลักสูตร</span>
        <span class="user-info">👤 {{ user?.name || 'กำลังโหลด...' }}</span>
      </header>
      
      <div class="page-content">
        <slot /> <!-- เนื้อหาของแต่ละหน้าจะมาโผล่ตรงนี้ -->
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useCookie } from '#app'

const router = useRouter()
// ดึงข้อมูล User จาก Cookie (Nuxt ชอบใช้ Cookie เพราะรองรับ SSR)
const user = useCookie('user_data')

const logout = () => {
  user.value = null // ลบ Cookie
  router.push('/login')
}
</script>

<style scoped>
.app-layout { display: flex; height: 100vh; }
.sidebar { width: 250px; background-color: #2c3e50; color: white; display: flex; flex-direction: column; }
.logo { padding: 20px; text-align: center; border-bottom: 1px solid #34495e; }
.menu { display: flex; flex-direction: column; padding: 20px 0; flex: 1; }
.menu a { color: #bdc3c7; text-decoration: none; padding: 12px 20px; }
.menu a:hover, .menu a.router-link-active { background-color: #34495e; color: white; border-left: 4px solid #e67e22; }
.logout-zone { padding: 20px; }
.btn-logout { width: 100%; padding: 10px; background: transparent; border: 1px solid #e74c3c; color: #e74c3c; border-radius: 5px; cursor: pointer; }
.btn-logout:hover { background: #e74c3c; color: white; }

.main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
.topbar { background: white; padding: 15px 20px; display: flex; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.user-info { font-weight: bold; color: #e67e22; }
.page-content { padding: 20px; }
/* 🌟 จัดขนาดโลโก้ใน Sidebar */
.sidebar-logo {
  width:150px; /* ปรับขนาดให้พอดีกับแถบด้านซ้าย */
  height: auto;
  margin-bottom: 10px;
  background-color: white; /* ถ้าโลโก้กลืนกับสีพื้นหลัง ให้เปิดสีพื้นหลังขาวแบบนี้ครับ */
  border-radius: 50%; /* ถ้าอยากให้กรอบเป็นวงกลม */
  padding: 5px;
}
</style>