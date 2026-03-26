<template>
  <div class="card data-card">
    <div class="card-header">ตาราง Mapping (CLO / ELO)</div>
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
        <button class="btn-orange">+ สร้างไฟล์ มคอ.2 (.docx)</button>
      </div>

      <table class="styled-table matrix-table">
        <thead>
          <tr>
            <th rowspan="2" colspan="2" style="width: 100px;">รายวิชา</th>
            <th rowspan="2" style="width: 30%;">คำอธิบาย (CLO)</th>
            <th colspan="8">ผลลัพธ์การเรียนรู้ระดับหลักสูตร (ELO)</th>
          </tr>
          <tr>
            <th v-for="i in 8" :key="i">ELO {{ i }}</th>
          </tr>
        </thead>
        
        <tbody v-for="(courseData, courseName) in filteredMapping" :key="courseName">
          <tr v-for="(clo, index) in courseData.clos" :key="clo.code">
            
            <td v-if="index === 0" :rowspan="courseData.clos.length" class="course-name-cell">
              <b>{{ courseName }}</b>
            </td>
            
            <td class="center clo-code"><b>{{ clo.code }}</b></td>
            <td class="clo-desc">{{ clo.desc }}</td>
            
            <td v-for="i in 8" :key="i" class="center map-icon">
              {{ getIcon(clo.elos['ELO ' + i]) }}
            </td>
            
          </tr>
        </tbody>
      </table>

      <div v-if="Object.keys(filteredMapping).length === 0" class="empty-state">
        ไม่มีข้อมูลตาราง Mapping ในปีการศึกษานี้
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const groupedData = ref({})
const selectedYear = ref('2568') // ตั้งต้นโชว์ปี 2568

// ฟังก์ชันแปลงตัวอักษรเป็นไอคอนจุด
const getIcon = (level) => {
  if (level === 'H') return '⚫'
  if (level === 'P') return '◐'
  if (level === 'L') return '⚪'
  return ''
}

// โหลดข้อมูลจาก Backend
onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/mapping')
    const rawData = await res.json()
    
    // จัดกลุ่มข้อมูล (Group By Course)
    const formatted = {}
    rawData.forEach(row => {
      const cName = row.name_en
      
      // ถ้าเพิ่งเคยเจอวิชานี้ครั้งแรก ให้สร้างกล่องข้อมูลเตรียมไว้
      if (!formatted[cName]) {
        formatted[cName] = { 
          academic_year: row.academic_year, // 📌 เก็บปีการศึกษาไว้ใช้กรองทีหลัง
          clos: [] 
        }
      }
      
      // หา CLO ในวิชานี้ ว่าเคยแอดเข้าไปหรือยัง
      let cloObj = formatted[cName].clos.find(c => c.code === row.clo_code)
      if (!cloObj) {
        cloObj = { code: row.clo_code, desc: row.clo_desc, elos: {} }
        formatted[cName].clos.push(cloObj)
      }
      
      // ยัดข้อมูลจุดดำ-ขาวลงไปใน ELO
      cloObj.elos[row.elo_code] = row.responsibility_level
    })
    
    groupedData.value = formatted
  } catch (error) {
    console.error('Error fetching mapping:', error)
  }
})

// 🌟 ตัวกรองข้อมูล (ทำงานอัตโนมัติเมื่อ selectedYear เปลี่ยน)
const filteredMapping = computed(() => {
  if (selectedYear.value === 'all') return groupedData.value
  
  const filtered = {}
  // วนลูปเช็คทีละวิชา ว่าปีการศึกษาตรงกับที่เลือกใน Dropdown ไหม
  for (const [courseName, data] of Object.entries(groupedData.value)) {
    if (data.academic_year == selectedYear.value) {
      filtered[courseName] = data
    }
  }
  return filtered
})
</script>

<style scoped>
.card { background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden; margin-top: 10px;}
.card-header { background-color: #e36c3e; color: white; padding: 12px 15px; font-weight: bold; font-size: 16px;}
.card-body { padding: 20px; overflow-x: auto; }
.toolbar { display: flex; justify-content: space-between; margin-bottom: 15px; }
.toolbar select { padding: 6px 10px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px;}
.btn-orange { background-color: #e36c3e; color: white; border: none; padding: 6px 15px; border-radius: 4px; cursor: pointer; font-weight: bold;}

.styled-table { width: 100%; border-collapse: collapse; font-size: 13px; min-width: 800px; }
.styled-table th, .styled-table td { border: 1px solid #ddd; padding: 6px 10px; }
.styled-table th { background-color: #f5f5f5; text-align: center; color: #333; }
.center { text-align: center; }

/* 🌟 จัดชื่อวิชาให้เป็นแนวนอน ชิดซ้าย-บน */
.course-name-cell { 
  text-align: left; 
  vertical-align: top; /* ดันข้อความให้ชิดบน */
  width: 280px; /* บังคับความกว้างไม่ให้แคบไป */
  font-size: 13px; 
  padding: 12px 15px !important; 
  background-color: #fafafa;
  line-height: 1.5; 
  white-space: normal; /* ให้ข้อความตัดขึ้นบรรทัดใหม่ได้ */
}

/* 🌟 ลดขนาดช่องและฟอนต์ของ CLO ลง */
.clo-desc { 
  color: #444; 
  width: 350px; /* บังคับความกว้างไม่ให้กว้างเกินไป */
  font-size: 12px; 
  line-height: 1.5;
  text-align: left;
  vertical-align: top; /* ดันข้อความให้ชิดบน */
}

.map-icon { 
  font-size: 18px; 
  width: 45px;
  vertical-align: middle;
}

.clo-code { font-size: 12px; color: #555; }
.clo-desc { color: #444; }
.map-icon { font-size: 16px; width: 40px;}
.empty-state { text-align: center; padding: 40px; color: #888; border: 1px dashed #ccc; margin-top: 10px; border-radius: 8px;}
</style>