export default defineNuxtRouteMiddleware((to, from) => {
  // 1. ดึงข้อมูลว่ามี Cookie ของคนที่ล็อกอินแล้วหรือยัง
  const user = useCookie('user_data')

  // 2. ถ้า "ไม่มีข้อมูล User" (ยังไม่ล็อกอิน) และ "กำลังจะไปหน้าที่ไม่ใช่ /login"
  if (!user.value && to.path !== '/login') {
    // 🛑 เตะกลับไปหน้า login ทันที
    return navigateTo('/login')
  }

  // 3. (แถมให้) ถ้า "มีข้อมูล User" (ล็อกอินแล้ว) แต่พยายามจะเข้าหน้า "/login" อีก
  if (user.value && to.path === '/login') {
    // 🟢 ให้เด้งไปหน้าแผงควบคุม (หน้าแรก) เลย ไม่ต้องล็อกอินซ้ำ
    return navigateTo('/')
  }
})