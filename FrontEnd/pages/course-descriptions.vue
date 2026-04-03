<template>
  <div class="page-container">
    
    <div class="header-actions">
      <h2>📖 คำอธิบายรายวิชา (Course Descriptions)</h2>
      <button class="btn-export">📥 Export to Word</button>
    </div>

    <div v-if="pending" style="text-align: center; padding: 50px;">
      กำลังดึงข้อมูลคำอธิบายรายวิชา... ⏳
    </div>

    <!-- 🌟 หน้ากระดาษจำลองเล่มหลักสูตร -->
    <div v-else class="document-paper">
      
      <div v-for="course in courses" :key="course.course_code" class="course-block">
        
        <!-- บรรทัดที่ 1: รหัส ชื่ออังกฤษ หน่วยกิต -->
        <div class="course-title-line">
          <span class="c-code">{{ course.course_code }}</span>
          <span class="c-name">{{ course.name_en }}</span>
          <span class="c-credit">{{ course.credits }}</span>
        </div>
        
        <!-- บรรทัดที่ 2: ชื่อไทย -->
        <div v-if="course.name_th" class="course-name-secondary">
          {{ course.name_th }}
        </div>
        
        <!-- 🌟 บรรทัดที่ 3: คำอธิบายภาษาไทย (เอาขึ้นมาก่อน) -->
        <div class="course-desc-line">
          {{ course.description || 'ยังไม่มีการระบุคำอธิบายรายวิชา...' }}
        </div>

        <!-- 🌟 บรรทัดที่ 4: คำอธิบายภาษาอังกฤษ (เอาไว้ด้านล่าง) -->
        <div class="course-desc-en">
          {{ course.description_en || 'No course description provided...' }}
        </div>
        
      </div>
      
    </div>

  </div>
</template>

<script setup>
import { useFetch } from '#app'

const { data: courses, pending } = await useFetch('http://127.0.0.1:8000/api/course-descriptions')
</script>

<style scoped>
.page-container { max-width: 900px; margin: 0 auto; padding-bottom: 50px; }

.header-actions { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.header-actions h2 { color: #2c3e50; margin: 0; }
.btn-export { background: #2980b9; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.btn-export:hover { background: #1f618d; }

/* สไตล์หน้ากระดาษ A4 */
.document-paper {
  background: white;
  padding: 40px 50px;
  border-radius: 4px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  font-family: 'Sarabun', 'Segoe UI', Tahoma, sans-serif; 
}

.course-block {
  margin-bottom: 30px; 
}

/* รหัส ชื่ออังกฤษ หน่วยกิต */
.course-title-line {
  display: flex;
  font-weight: bold;
  font-size: 16px;
  color: #000;
}

.c-code { width: 100px; flex-shrink: 0; } 
.c-name { flex-grow: 1; } 
.c-credit { width: 80px; text-align: right; flex-shrink: 0; } 

/* ชื่อภาษาไทย */
.course-name-secondary {
  font-weight: bold;
  font-size: 15px;
  color: #34495e;
  margin-left: 100px;
  margin-bottom: 5px;
}

/* 🌟 คำอธิบายวิชาภาษาไทย (เพิ่ม margin-bottom ให้ห่างจากภาษาอังกฤษนิดนึง) */
.course-desc-line {
  font-size: 15px;
  color: #333;
  line-height: 1.6;
  text-indent: 40px; 
  text-align: justify; 
  margin-bottom: 5px; 
}

/* 🌟 คำอธิบายวิชาภาษาอังกฤษ (ตัวเอียง) */
.course-desc-en {
  font-size: 15px;
  color: #555;
  line-height: 1.6;
  text-indent: 40px; 
  text-align: justify; 
  font-style: italic; 
}
</style>