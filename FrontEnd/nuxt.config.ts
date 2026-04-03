// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  app: {
    head: {
      title: 'ระบบจัดการหลักสูตร', // เปลี่ยนชื่อเว็บตรงนี้ได้เลย
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/img/logo.ico' }
      ]
    }
  }
})
