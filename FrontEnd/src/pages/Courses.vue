<template>
  <div class="card data-card">
    <div class="card-header">รายวิชาทั้งหมด</div>
    <div class="card-body">
      
      <div class="toolbar">
        <div>
          <label>ปีการศึกษา </label>
          <select v-model="selectedYear">
            <option value="2567">2567</option>
            <option value="2568">2568</option>
            <option value="all">ดูทั้งหมด</option>
          </select>
        </div>
        <button class="btn-orange">+ เพิ่มรายวิชา</button>
      </div>

      <table class="styled-table">
        <thead>
          <tr>
            <th style="width: 150px;">รหัสวิชา</th>
            <th style="width: 80px;">ตอนเรียน</th>
            <th>ชื่อวิชา</th>
            <th style="width: 100px;">หน่วยกิต</th>
            <th style="width: 80px;">จัดการ</th>
          </tr>
        </thead>
        <tbody v-for="course in filteredCourses" :key="course.course_code">
          
          <tr class="course-row">
            <td>
              <button class="toggle-btn" @click="toggleCourse(course.course_id)">
                {{ course.isExpanded ? '🔽' : '▶️' }}
              </button>
              <b>{{ course.course_code }}</b>
            </td>
            <td class="center"><b>{{ course.section }}</b></td>
            <td><b>{{ course.name_en }}</b><br><span style="font-size: 12px; color: #666;">{{ course.name_th }}</span></td>
            <td class="center"><b>{{ course.credits }}</b></td>
            <td class="center action-icons">✏️ 🗑️</td>
          </tr>

          <tr v-show="course.isExpanded" v-for="clo in course.clos" :key="clo.clo_code" class="clo-row">
            <td class="center text-muted">{{ clo.clo_code }}</td>
            <td></td>
            <td class="text-muted">{{ clo.description }}</td>
            <td></td>
            <td class="center action-icons">✏️ 🗑️</td>
          </tr>
          
        </tbody>
      </table>
      
      <div v-if="filteredCourses.length === 0" class="empty-state">
        ไม่มีข้อมูลรายวิชาในปีการศึกษานี้
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const courses = ref([])
const selectedYear = ref('2568') // ตั้งค่าเริ่มต้นให้โชว์ปี 2568

// ฟังก์ชันดึงข้อมูลจาก API
onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/courses')
    const data = await res.json()
    
    // เติมตัวแปร isExpanded = true เข้าไปในทุกวิชา เพื่อให้ตอนเริ่มแรกมันกางออกทั้งหมด (หรือตั้งเป็น false ถ้าอยากให้มันหุบตอนแรก)
    courses.value = data.map(course => ({
      ...course,
      isExpanded: true 
    }))
  } catch (error) {
    console.error('Error fetching courses:', error)
  }
})

// 🌟 ฟังก์ชันกรองวิชาตามปีการศึกษา
const filteredCourses = computed(() => {
  if (selectedYear.value === 'all') return courses.value
  return courses.value.filter(course => course.academic_year == selectedYear.value)
})

// 🌟 ฟังก์ชันสลับสถานะ กาง/หุบ (Toggle)
const toggleCourse = (courseId) => {
  const targetCourse = courses.value.find(c => c.course_id === courseId)
  if (targetCourse) {
    targetCourse.isExpanded = !targetCourse.isExpanded
  }
}
</script>

<style scoped>
.card { background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden; margin-top: 10px;}
.card-header { background-color: #e36c3e; color: white; padding: 12px 15px; font-weight: bold; font-size: 16px;}
.card-body { padding: 20px; }
.toolbar { display: flex; justify-content: space-between; margin-bottom: 15px; }
.toolbar select { padding: 6px 10px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px;}
.btn-orange { background-color: #e36c3e; color: white; border: none; padding: 6px 15px; border-radius: 4px; cursor: pointer; font-weight: bold;}

.styled-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.styled-table th, .styled-table td { border: 1px solid #ddd; padding: 10px; }
.styled-table th { background-color: #f5f5f5; text-align: center; color: #333; }
.center { text-align: center; }

/* แต่งปุ่มลูกศร Toggle */
.toggle-btn { background: #0056b3; color: white; border: none; border-radius: 3px; cursor: pointer; padding: 2px 5px; margin-right: 5px; font-size: 10px;}
.course-row { background-color: #fff; }
.clo-row { background-color: #fafafa; }
.text-muted { color: #555; font-size: 13px; }
.action-icons { cursor: pointer; letter-spacing: 5px; }
.empty-state { text-align: center; padding: 30px; color: #888; border: 1px dashed #ccc; margin-top: 10px; }
</style>