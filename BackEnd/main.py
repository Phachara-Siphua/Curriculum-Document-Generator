from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CIT Curriculum API")

# 🌟 1. เปิดประตู CORS ให้ Frontend (Vue.js) สามารถยิง API เข้ามาได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # อนุญาตทุก Origin (ใช้เฉพาะตอนกำลังพัฒนาระบบ)
    allow_credentials=True,
    allow_methods=["*"], # อนุญาตทุก Method (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# 🌟 2. สร้างโครงร่าง (Schema) สำหรับรับข้อมูลจากหน้า Login ของ Vue.js
class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Welcome to CIT Curriculum Backend"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT VERSION()")).fetchone()
        return {"status": "success", "message": "เชื่อมต่อ MariaDB สำเร็จ!", "db_version": result[0]}
    except Exception as e:
        return {"status": "error", "message": f"เชื่อมต่อล้มเหลว: {str(e)}"}

# 🌟 3. สร้าง API สำหรับหน้า Login (เชื่อมต่อ Database จริง)
@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)): # ✨ อย่าลืมเพิ่ม db: Session ตรงนี้
    # ใช้คำสั่ง SQL ค้นหาข้อมูลจากตาราง users
    query = text("""
        SELECT id, username, name, role 
        FROM users 
        WHERE username = :username AND password = :password
    """)
    
    # รันคำสั่ง SQL โดยเอา username/password ที่หน้าเว็บส่งมา ไปเช็คกับตารางใน Database
    user = db.execute(query, {"username": request.username, "password": request.password}).fetchone()
    
    if user:
        # ถ้าเจอข้อมูล (รหัสถูกต้อง) ให้ส่งข้อมูล user กลับไป
        user_dict = user._mapping
        return {
            "status": "success", 
            "message": "เข้าสู่ระบบสำเร็จ", 
            "user_data": {
                "name": user_dict["name"], 
                "role": user_dict["role"]
            }
        }
    else:
        # ถ้าไม่เจอข้อมูล (User ไม่มี หรือ รหัสผิด)
        return {
            "status": "error", 
            "message": "Username หรือ Password ไม่ถูกต้อง"
        }
    
# 🌟 4. สร้าง API Path: /courses เพื่อดึงข้อมูลวิชาทั้งหมดพร้อม CLO
@app.get("/courses")
def get_all_courses(db: Session = Depends(get_db)):
    # ✨ เพิ่ม c.section เข้าไปในคำสั่ง SELECT
    query = text("""
        SELECT c.id as course_id, c.course_code, c.section, c.name_th, c.name_en, c.credits, c.academic_year, 
               clos.id as clo_id, clos.clo_code, clos.description as clo_desc
        FROM courses c 
        JOIN clos ON c.id = clos.course_id
    """)
    result = db.execute(query).fetchall()
    
    courses_dict = {}
    for row in result:
        row_dict = row._mapping
        course_id = row_dict["course_id"]
        
        if course_id not in courses_dict:
            courses_dict[course_id] = {
                "course_id": course_id,
                "course_code": row_dict["course_code"],
                "section": row_dict["section"], # ✨ เก็บข้อมูลตอนเรียนไว้ส่งให้หน้าเว็บ
                "name_th": row_dict["name_th"],
                "name_en": row_dict["name_en"],
                "credits": row_dict["credits"],
                "academic_year": row_dict["academic_year"],
                "clos": [] 
            }
        
        courses_dict[course_id]["clos"].append({
            "clo_code": row_dict["clo_code"],
            "description": row_dict["clo_desc"]
        })
    
    return list(courses_dict.values())

# 🌟 5. สร้าง API Path: /mapping เพื่อดึงข้อมูลตาราง Mapping ทั้งหมดพร้อม ELO-CLO
@app.get("/mapping")
def get_mapping_table(db: Session = Depends(get_db)):
    # ✨ เพิ่ม c.academic_year เข้ามาใน SELECT
    query = text("""
        SELECT c.course_code, c.name_en, c.academic_year, 
               clos.clo_code, clos.description as clo_desc, 
               elos.elo_code, elos.description as elo_desc, mappings.responsibility_level
        FROM mappings 
        JOIN clos ON mappings.clo_id = clos.id
        JOIN courses c ON clos.course_id = c.id
        JOIN elos ON mappings.elo_id = elos.id
    """)
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]