from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ตั้งค่าการเชื่อมต่อ DB
# รูปแบบ: mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
# สมมติใช้ XAMPP ปกติ user คือ root และไม่มีรหัสผ่าน
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/cit_curriculum"

# สร้าง Engine สำหรับเชื่อมต่อ
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# สร้าง Session ไว้คุยกับ DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class สำหรับให้ไฟล์อื่นนำไปสร้างตาราง (Table Models)
Base = declarative_base()

# ฟังก์ชันสำหรับดึง Database Session ไปใช้ใน API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()