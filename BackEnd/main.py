from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# 🌟 ตั้งค่าการเชื่อมต่อ Database (สมมติว่าใช้ XAMPP user:root รหัสผ่านว่าง)
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/cit_curriculum"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title="Curriculum Document Generator API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

# 🌟 1. API ล็อกอิน (เช็คจาก Database จริง)
@app.post("/api/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    query = text("SELECT * FROM users WHERE username = :username AND password = :password")
    user = db.execute(query, {"username": request.username, "password": request.password}).fetchone()
    
    if user:
        user_dict = user._mapping
        return {
            "status": "success", 
            "user_data": {"name": user_dict["name"], "role": user_dict["role"]}
        }
    return {"status": "error", "message": "Username หรือ Password ไม่ถูกต้อง"}

# 🌟 2. API ดึงข้อมูลรายวิชาและ Mapping
@app.get("/api/courses")
def get_courses(db: Session = Depends(get_db)):
    # ดึงข้อมูลทั้งหมดโดย JOIN ตาราง courses, clos, และ mappings เข้าด้วยกัน
    query = text("""
        SELECT c.id as course_id, c.course_code, c.name_en, c.section, c.academic_year,
               cl.id as clo_id, cl.clo_code, cl.description,
               m.map_type, m.target_num
        FROM courses c
        LEFT JOIN clos cl ON c.id = cl.course_id
        LEFT JOIN mappings m ON cl.id = m.clo_id
        ORDER BY c.course_code, cl.clo_code
    """)
    results = db.execute(query).fetchall()

    courses_dict = {}
    for row in results:
        r = row._mapping
        c_id = r["course_id"]
        
        # สร้างโครงสร้างรายวิชา
        if c_id not in courses_dict:
            courses_dict[c_id] = {
                "id": c_id,
                "code": r["course_code"],
                "name": r["name_en"],
                "section": r["section"],
                "academic_year": r["academic_year"],
                "isExpanded": True, # ให้กางออกตอนแรก
                "clos": {}
            }
        
        clo_id = r["clo_id"]
        if clo_id and clo_id not in courses_dict[c_id]["clos"]:
            courses_dict[c_id]["clos"][clo_id] = {
                "id": clo_id,
                "code": r["clo_code"],
                "desc": r["description"],
                "plos": [],
                "ylos": []
            }
            
        # เติมจุด Mapping
        if r["map_type"] == 'PLO' and r["target_num"] not in courses_dict[c_id]["clos"][clo_id]["plos"]:
            courses_dict[c_id]["clos"][clo_id]["plos"].append(r["target_num"])
        elif r["map_type"] == 'YLO' and r["target_num"] not in courses_dict[c_id]["clos"][clo_id]["ylos"]:
            courses_dict[c_id]["clos"][clo_id]["ylos"].append(r["target_num"])

    # แปลงโครงสร้างให้ Nuxt อ่านง่าย (แปลง dict ของ CLO ให้เป็น list)
    final_courses = []
    for c in courses_dict.values():
        c["clos"] = list(c["clos"].values())
        final_courses.append(c)

    return final_courses

# 🌟 3. API ดึงข้อมูลวิชาแบบเจาะจง 1 วิชา (พร้อม CLO)
@app.get("/api/courses/{course_id}")
def get_course_detail(course_id: int, db: Session = Depends(get_db)):
    # ดึงข้อมูลวิชาหลัก
    course_query = text("SELECT * FROM courses WHERE id = :id")
    course = db.execute(course_query, {"id": course_id}).fetchone()
    
    if not course:
        return {"status": "error", "message": "ไม่พบรายวิชา"}
        
    c_dict = course._mapping
    
    # ดึงข้อมูล CLO ของวิชานี้
    clo_query = text("SELECT * FROM clos WHERE course_id = :id")
    clos = db.execute(clo_query, {"id": course_id}).fetchall()
    
    clo_list = [{"id": row.id, "code": row.clo_code, "desc": row.description} for row in clos]
    
    return {
        "status": "success",
        "course": {
            "id": c_dict["id"],
            "code": c_dict["course_code"],
            "name": c_dict["name_en"],
            "section": c_dict["section"],
            "academic_year": c_dict["academic_year"],
            "clos": clo_list
        }
    }

# 🌟 4. API ดึงคำอธิบายรายวิชาทั้งหมด (สำหรับจัดหน้าเล่มหลักสูตร)
@app.get("/api/course-descriptions")
def get_course_descriptions(db: Session = Depends(get_db)):
    # เลือกข้อมูลทั้งไทยและอังกฤษ
    query = text("""
        SELECT DISTINCT course_code, name_th, name_en, credits, description, description_en 
        FROM courses 
        ORDER BY course_code
    """)
    results = db.execute(query).fetchall()
    
    return [dict(row._mapping) for row in results]