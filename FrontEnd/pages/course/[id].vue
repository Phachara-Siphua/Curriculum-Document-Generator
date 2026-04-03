<template>
  <div class="page-container">
    
    <div class="wizard-container">
      <div class="wizard-step text-muted">1. โครงสร้างหลักสูตร</div>
      <div class="wizard-step text-muted">2. จัดการรายวิชา & Mapping</div>
      <div class="wizard-step active">3. รายละเอียดรายวิชา (สอน)</div>
      <div class="wizard-step text-muted">4. สร้างเอกสาร มคอ.2</div>
    </div>

    <!-- 🌟 ระหว่างรอ API โหลดข้อมูล ให้โชว์คำนี้ -->
    <div v-if="pending" style="text-align: center; padding: 50px;">
      กำลังโหลดข้อมูลรายวิชา... ⏳
    </div>

    <div v-else-if="data?.status === 'success'">
      <!-- 🌟 หัวข้อรายวิชา (ดึงจาก Database จริง) -->
      <div class="course-header">
        <h2>รายละเอียดรายวิชา: 
          <span class="text-primary">{{ data.course.code }} {{ data.course.name }} ( Sec {{ data.course.section }} )</span>
        </h2>
      </div>

      <!-- ระบบ Tabs นำทาง -->
      <div class="tabs-container">
        <button :class="['tab-btn', { active: activeTab === 'clos' }]" @click="activeTab = 'clos'">CLOs</button>
        <button :class="['tab-btn', { active: activeTab === 'lesson' }]" @click="activeTab = 'lesson'">แผนการสอน</button>
        <button :class="['tab-btn', { active: activeTab === 'grading' }]" @click="activeTab = 'grading'">สัดส่วนคะแนน</button>
      </div>

      <!-- 🟢 เนื้อหา Tab: CLOs -->
      <div v-if="activeTab === 'clos'" class="tab-content">
        <div class="action-bar">
          <button class="btn-dark">+ เพิ่ม CLO</button>
          <button class="btn-primary" @click="saveData">💾 บันทึกข้อมูล</button>
        </div>

        <!-- 🌟 วนลูป CLO จาก Database จริง -->
        <div v-for="clo in data.course.clos" :key="clo.id" class="clo-card">
          <div class="clo-card-header">
            <span class="clo-title">{{ clo.code }}: [Rich Text Editor Field]</span>
            <span class="badge-orange">ℹ️ TABEE/ABET requirements</span>
          </div>
          <!-- 🌟 สังเกต v-model จะผูกกับ desc ของแต่ละ clo -->
          <textarea v-model="clo.desc" class="textarea-mock" rows="4"></textarea>
        </div>
        
        <div v-if="data.course.clos.length === 0" class="blank-state">
          วิชานี้ยังไม่มีการระบุ CLO (กรุณากด + เพิ่ม CLO)
        </div>
      </div>

      <!-- 🟢 ส่วนเนื้อหา Tab: อื่นๆ -->
      <div v-if="activeTab === 'lesson'" class="tab-content blank-state">
        <h3>📅 แผนการสอน (Lesson Plan)</h3>
        <p class="text-muted">กำลังพัฒนาระบบกรอกแผนการสอน...</p>
      </div>

      <div v-if="activeTab === 'grading'" class="tab-content blank-state">
        <h3>📊 สัดส่วนคะแนน (Grading)</h3>
        <p class="text-muted">กำลังพัฒนาระบบกำหนดคะแนน...</p>
      </div>
    </div>
    
    <div v-else class="blank-state" style="color: red;">
      ❌ ไม่พบข้อมูลรายวิชานี้
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useFetch } from '#app'

const route = useRoute()
const courseId = route.params.id // 🌟 ดึง ID จาก URL (เช่น /course/1 จะได้เลข 1)
const activeTab = ref('clos')

// 🌟 ดึงข้อมูลจาก FastAPI ตาม ID ที่ได้มา
const { data, pending } = await useFetch(`http://127.0.0.1:8000/api/courses/${courseId}`)

const saveData = () => {
  // แสดงข้อมูลใน Console ให้ดูว่าเราแก้ข้อความแล้วมันเปลี่ยนจริงๆ
  console.log("ข้อมูลที่จะส่งไปอัปเดต:", data.value.course.clos)
  alert('จำลองการบันทึก! (ดูข้อมูลที่จะเซฟใน Console)')
}
</script>

<style scoped>
.page-container { max-width: 1000px; margin: 0 auto; padding-bottom: 50px; }
.wizard-container { display: flex; gap: 20px; margin-bottom: 20px; border-bottom: 2px solid #ddd; padding-bottom: 15px; }
.wizard-step { font-size: 14px; font-weight: bold; padding: 5px 10px; }
.wizard-step.active { color: #8e44ad; border-bottom: 3px solid #8e44ad; }
.text-muted { color: #95a5a6; }
.text-primary { color: #2980b9; }

.course-header { background: white; padding: 20px; border-radius: 8px 8px 0 0; border-bottom: 1px solid #eee; }
.course-header h2 { margin: 0; font-size: 20px; color: #2c3e50; }

.tabs-container { display: flex; background: white; padding: 0 20px; border-bottom: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.tab-btn { background: none; border: none; padding: 15px 20px; font-size: 15px; font-weight: bold; color: #7f8c8d; cursor: pointer; border-bottom: 3px solid transparent; transition: 0.2s; }
.tab-btn:hover { color: #8e44ad; }
.tab-btn.active { color: #8e44ad; border-bottom-color: #8e44ad; }

.tab-content { background: white; padding: 25px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.blank-state { text-align: center; padding: 50px; }

.action-bar { display: flex; justify-content: flex-end; gap: 10px; margin-bottom: 20px; }
.btn-dark { background: #34495e; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.btn-primary { background: #e67e22; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.btn-primary:hover { background: #d35400; }

.clo-card { border: 1px solid #e0e0e0; border-radius: 6px; padding: 15px; margin-bottom: 15px; background: #fafafa; }
.clo-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.clo-title { font-weight: bold; color: #2c3e50; }
.badge-orange { background: #fdf3e8; color: #e67e22; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid #fadbd8; }

.textarea-mock { width: 100%; border: 1px solid #ccc; border-radius: 4px; padding: 10px; font-size: 14px; font-family: inherit; resize: vertical; box-sizing: border-box; }
.textarea-mock:focus { outline: none; border-color: #8e44ad; box-shadow: 0 0 0 2px rgba(142, 68, 173, 0.1); }
</style>