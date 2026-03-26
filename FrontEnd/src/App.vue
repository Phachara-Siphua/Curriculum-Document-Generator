<template>
  <div class="app-layout">
    <SideBar />
    <main class="main-content">
      <TopBar />
      <div class="content-body">
        <router-view></router-view> 
      </div>
    </main>
  </div>
</template>

<script setup>
import SideBar from './components/SideBar.vue'
import TopBar from './components/TopBar.vue'
</script>

<style>
/* รีเซ็ตค่าเริ่มต้นของเบราว์เซอร์ */
html, body { 
  margin: 0; 
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
  background-color: #b3b3b3; /* สีเทาตามรูป mockup */
}

/* ปลดล็อกคอนเทนเนอร์หลักของ Vue ให้เต็มจอ */
#app {
  max-width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  width: 100%;
  height: 100vh;
}

/* โครงสร้าง Layout หลัก */
.app-layout { 
  display: flex; 
  height: 100vh; 
  width: 100%;
}

/* พื้นที่ทำงานด้านขวา */
.main-content { 
  flex: 1; /* บังคับให้ขยายจนเต็มพื้นที่ที่เหลือจาก Sidebar */
  display: flex; 
  flex-direction: column; 
  overflow-y: auto; 
}

.content-body { 
  padding: 0 15px 15px 15px; 
  flex: 1; /* ยืดเนื้อหาให้เต็มความสูง */
}
</style>