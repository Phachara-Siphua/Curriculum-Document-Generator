<template>
  <div class="page-container">
    
    <div class="wizard-container">
      <div class="wizard-step text-muted">1. โครงสร้างหลักสูตร (PLO/YLO)</div>
      <div class="wizard-step active">2. จัดการรายวิชา & Mapping (Grid View)</div>
      <div class="wizard-step text-muted">3. รายละเอียดรายวิชา (สอน)</div>
      <div class="wizard-step text-muted">4. สร้างเอกสาร มคอ.2</div>
    </div>

    <!-- แจ้งเตือนสิทธิ์การใช้งาน -->
    <div v-if="!canEdit" class="alert-warning">
      🔒 คุณกำลังเข้าใช้งานในโหมด <b>"ดูได้อย่างเดียว (Viewer)"</b> ไม่สามารถแก้ไขหรือเพิ่มข้อมูลได้
    </div>

    <div class="header-actions">
      <div>
        <label class="filter-label">ปีการศึกษา</label>
        <select v-model="selectedYear" class="filter-select">
          <option value="all">ดูทั้งหมด</option>
          <option value="2568">2568</option>
          <option value="2567">2567</option>
        </select>
      </div>
      <!-- 🌟 ซ่อนปุ่มเพิ่มรายวิชา ถ้าไม่มีสิทธิ์แก้ไข -->
      <button v-if="canEdit" class="btn-primary">+ เพิ่มรายวิชาใหม่</button>
    </div>

    <!-- โชว์ข้อความกำลังโหลดตอนรอ API -->
    <div v-if="pending" style="text-align: center; padding: 50px;">กำลังโหลดข้อมูล... ⏳</div>

    <div v-else class="table-card">
      <table class="mapping-table">
        <thead>
          <tr>
            <th rowspan="2" style="width: 250px;">รายวิชา / ตอนเรียน</th>
            <th rowspan="2" style="width: 80px;">CLO ID</th>
            <th rowspan="2" style="width: 300px;">คำอธิบายผลลัพธ์การเรียนรู้ (CLO)</th>
            <th colspan="8" class="plo-header">ผลลัพธ์หลักสูตร (PLO)</th>
            <th colspan="8" class="ylo-header">ผลลัพธ์รายปี (YLO)</th>
          </tr>
          <tr>
            <th v-for="i in 8" :key="'ph'+i" class="sub-th">{{ i }}</th>
            <th v-for="i in 8" :key="'yh'+i" class="sub-th">{{ i }}</th>
          </tr>
        </thead>
        
        <tbody v-for="course in filteredCourses" :key="course.id">
          <tr class="course-header-row" @click="toggleCourse(course)">
            <td colspan="19" class="course-title-cell">
              <span class="toggle-icon">{{ course.isExpanded ? '🔽' : '▶️' }}</span>
              <span class="course-code">{{ course.code }}</span>
              <span class="course-name">{{ course.name }}</span>
              <span class="course-sec">(Sec {{ course.section }})</span>
              
              <!-- 🌟 ปุ่มใหม่เอาไว้กดไปหน้ารายละเอียดวิชา -->
              <NuxtLink :to="`/course/${course.id}`" class="btn-edit-course" @click.stop>
                ✏️ จัดการรายละเอียดวิชา
              </NuxtLink>
            </td>
          </tr>

          <tr v-show="course.isExpanded" v-for="clo in course.clos" :key="clo.id" class="clo-row">
            <td class="empty-indent"></td>
            <td class="clo-code"><b>{{ clo.code }}</b></td>
            <td class="clo-desc">{{ clo.desc }}</td>
            
            <td v-for="p in 8" :key="'p'+p" class="center-align">
              <div class="circle" 
                   :class="{'active-plo': clo.plos.includes(p), 'disabled-circle': !canEdit}"
                   @click="toggleMapping(clo, 'plos', p)">
              </div>
            </td>
            
            <td v-for="y in 8" :key="'y'+y" class="center-align">
              <div class="circle" 
                   :class="{'active-ylo': clo.ylos.includes(y), 'disabled-circle': !canEdit}"
                   @click="toggleMapping(clo, 'ylos', y)">
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCookie } from '#app'

// 🌟 1. ดึงสิทธิ์ User เพื่อเช็คว่าแก้ไขได้ไหม
const user = useCookie('user_data')
const canEdit = computed(() => user.value?.role === 'admin')

// 🌟 2. สร้างตัวแปรเก็บข้อมูลและสถานะโหลด (แบบ Reactivity 100%)
const courses = ref([])
const pending = ref(true)

// โหลดข้อมูลตอนเปิดหน้าเว็บมาครั้งแรก (ใช้ onMounted + $fetch)
onMounted(async () => {
  try {
    // ใช้ $fetch ข้อมูลจะเป็นอิสระ ไม่ถูกล็อกโดย Nuxt
    const data = await $fetch('http://127.0.0.1:8000/api/courses')
    courses.value = data
  } catch (error) {
    console.error('Error fetching courses:', error)
  } finally {
    pending.value = false
  }
})

// 🌟 3. ระบบ Filter ปีการศึกษา
const selectedYear = ref('all')
const filteredCourses = computed(() => {
  if (courses.value.length === 0) return []
  if (selectedYear.value === 'all') return courses.value
  return courses.value.filter(c => c.academic_year.toString() === selectedYear.value)
})

// 🌟 4. ฟังก์ชันเปิด/ปิดรายวิชา (ตอนนี้หน้าเว็บจะกาง/ยุบ ตามแล้ว!)
const toggleCourse = (course) => {
  course.isExpanded = !course.isExpanded
}

// 🌟 5. ฟังก์ชันกดจุด Mapping (เช็คสิทธิ์ก่อนทำ)
const toggleMapping = (clo, type, value) => {
  if (!canEdit.value) return // ❌ ถ้าไม่มีสิทธิ์ ห้ามกดเปลี่ยนจุด!

  const index = clo[type].indexOf(value)
  if (index > -1) {
    clo[type].splice(index, 1) // เอาจุดออก
  } else {
    clo[type].push(value) // เพิ่มจุด
  }
}
</script>

<style scoped>
.page-container { max-width: 1200px; margin: 0 auto; }
.wizard-container { display: flex; gap: 20px; margin-bottom: 20px; border-bottom: 2px solid #ddd; padding-bottom: 15px; }
.wizard-step { font-size: 14px; font-weight: bold; padding: 5px 10px; }
.wizard-step.active { color: #8e44ad; border-bottom: 3px solid #8e44ad; }
.text-muted { color: #95a5a6; }

/* 🌟 กล่องแจ้งเตือนสิทธิ์ */
.alert-warning { background-color: #fff3cd; color: #856404; padding: 12px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #ffeeba; font-size: 14px; }

.header-actions { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.filter-label { font-size: 14px; font-weight: bold; color: #34495e; margin-right: 8px; }
.filter-select { padding: 6px 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
.btn-primary { background: #e67e22; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; }
.btn-primary:hover { background: #d35400; }

.table-card { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); overflow-x: auto; }
.mapping-table { width: 100%; border-collapse: collapse; min-width: 1000px; font-size: 13px; }
.mapping-table th, .mapping-table td { border: 1px solid #ecf0f1; padding: 10px; }
.mapping-table thead th { background-color: #f8f9fa; color: #2c3e50; text-align: center; }
.plo-header { background-color: #f4e8fb !important; color: #8e44ad !important; }
.ylo-header { background-color: #fdf3e8 !important; color: #e67e22 !important; }
.sub-th { font-size: 12px; font-weight: normal; color: #7f8c8d; }

.course-header-row { background-color: #ecf0f1; cursor: pointer; transition: 0.2s; }
.course-header-row:hover { background-color: #e2e6e8; }
.course-title-cell { padding: 12px 15px !important; }
.toggle-icon { font-size: 12px; margin-right: 10px; color: #7f8c8d; }
.course-code { font-weight: bold; color: #2c3e50; margin-right: 10px; }
.course-name { font-weight: bold; color: #2980b9; }
.course-sec { font-size: 12px; color: #e67e22; margin-left: 10px; }

.clo-row { background-color: white; }
.empty-indent { background-color: #fbfbfb; border-right: none !important; }
.clo-code { text-align: center; color: #7f8c8d; }
.clo-desc { color: #34495e; line-height: 1.5; }
.center-align { text-align: center; vertical-align: middle; }

/* 🌟 สไตล์วงกลม (เพิ่ม Disabled State) */
.circle { width: 14px; height: 14px; border-radius: 50%; border: 2px solid #bdc3c7; margin: 0 auto; cursor: pointer; transition: 0.2s; }
.circle:not(.disabled-circle):hover { border-color: #7f8c8d; transform: scale(1.2); }
.circle.active-plo { background-color: #8e44ad; border-color: #8e44ad; }
.circle.active-ylo { background-color: #e67e22; border-color: #e67e22; }
.disabled-circle { cursor: not-allowed; opacity: 0.7; }
.btn-edit-course {
  margin-left: auto; /* ดันปุ่มไปชิดขวาสุด */
  float: right;
  background: #f39c12;
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 12px;
  transition: 0.2s;
}
.btn-edit-course:hover { background: #d35400; }
</style>