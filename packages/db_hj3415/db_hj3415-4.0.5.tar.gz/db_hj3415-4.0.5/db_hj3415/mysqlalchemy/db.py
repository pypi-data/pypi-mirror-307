# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 연결
DATABASE_URL = "sqlite:///mysqlite.db"  # 또는 다른 데이터베이스 URL

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 세션을 사용하는 방법 예시
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()