<template>
  <aside class="sidebar">
    <div class="logo-container">
      <img src="../img/LOGO-CIT.png" alt="CIT Logo" class="cit-logo">
      <h3 class="app-title">Curriculum<br>Document Generator</h3>
    </div>
    
    <nav class="menu">
      <router-link to="/" active-class="active"><span class="icon">🏠</span> หน้าแรก</router-link>
      
      <router-link v-if="!authStore.isLoggedIn" to="/login" active-class="active"><span class="icon">🚪</span> เข้าสู่ระบบ</router-link>
      
      <router-link v-if="authStore.isLoggedIn" to="/courses" active-class="active"><span class="icon">📄</span> ข้อมูลหลักสูตร</router-link>
      <router-link v-if="authStore.isLoggedIn" to="/mapping" active-class="active"><span class="icon">🔠</span> ตาราง Mapping</router-link>
    </nav>
  </aside>
</template>

<script setup>
import { authStore } from '../store'
</script>

<style scoped>
.sidebar { width: 250px; background-color: #333333; color: white; display: flex; flex-direction: column; height: 100vh; }
.logo-container { padding: 25px 20px 15px 20px; text-align: center; }
.cit-logo { max-width: 90px; height: auto; margin-bottom: 10px; background-color: white; border-radius: 50%; padding: 5px; }
.app-title { margin: 0; font-size: 14px; font-weight: bold; color: white; line-height: 1.4; }

.menu { display: flex; flex-direction: column; padding: 10px 0; }
.menu a { color: #ccc; text-decoration: none; padding: 12px 20px; font-size: 15px; transition: 0.2s; display: flex; align-items: center; }
.icon { margin-right: 10px; font-size: 18px; }
.menu a:hover { background-color: #444; color: white; }
.menu a.active { background-color: #555; border-left: 4px solid #b3b3b3; color: white; }
</style>