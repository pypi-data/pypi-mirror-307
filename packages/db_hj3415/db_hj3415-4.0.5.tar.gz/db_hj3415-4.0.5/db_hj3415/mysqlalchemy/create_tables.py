# create_tables.py - 이 코드는 한번만 실행되어 테이블을 생성하면 다음에는 실행할 필요 없다.
from db_hj3415.mysqlalchemy.db import engine
from db_hj3415.mysqlalchemy.models import Base

# 데이터베이스에 테이블 생성
def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == '__main__':
    create_tables()

