from db import SessionLocal
from models import Log
from datetime import datetime, timedelta, timezone

def create_log(log_level, message, source=None):
    db = SessionLocal()
    try:
        # 로그 생성
        new_log = Log(log_level=log_level, message=message, source=source)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        print(f"Log created: {new_log}")
    finally:
        db.close()


def delete_log_by_id(log_id):
    db = SessionLocal()
    try:
        # 삭제할 로그 선택
        log_to_delete = db.query(Log).filter(Log.id == log_id).first()

        if log_to_delete:
            db.delete(log_to_delete)
            db.commit()
            print(f"Log with ID {log_id} deleted successfully.")
        else:
            print(f"No log found with ID {log_id}")
    finally:
        db.close()


def delete_old_logs(days):
    db = SessionLocal()
    try:
        # 특정 기간 이전의 로그 삭제
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        deleted_logs = db.query(Log).filter(Log.timestamp < cutoff_date).delete()

        db.commit()  # 변경 사항을 저장
        print(f"{deleted_logs} logs older than {days} days deleted successfully.")
    finally:
        db.close()


def delete_all_logs():
    db = SessionLocal()
    try:
        # logs 테이블의 모든 데이터 삭제
        deleted_logs = db.query(Log).delete()
        db.commit()  # 변경 사항을 저장
        print(f"All logs deleted successfully. Total logs deleted: {deleted_logs}")
    finally:
        db.close()


def get_logs():
    db = SessionLocal()
    try:
        # 모든 로그 가져오기
        logs = db.query(Log).all()
        return logs
    finally:
        db.close()

def get_logs_by_level(log_level):
    db = SessionLocal()
    try:
        # 특정 로그 수준의 로그만 가져오기
        logs = db.query(Log).filter(Log.log_level == log_level).all()
        return logs
    finally:
        db.close()

def get_recent_logs(days):
    db = SessionLocal()
    try:
        # 특정 날짜 이후의 로그 가져오기
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        logs = db.query(Log).filter(Log.timestamp >= cutoff_date).all()
        return logs
    finally:
        db.close()

def get_logs_paginated(page, page_size):
    db = SessionLocal()
    try:
        # 페이징을 적용하여 로그 가져오기
        logs = db.query(Log).offset((page - 1) * page_size).limit(page_size).all()
        return logs
    finally:
        db.close()


if __name__ == '__main__':
    # 예시: 로그 추가
    create_log("ERROR", "An error occurred in the system", "app.py")
    create_log("INFO", "System started", "system")
    # 예시: ID가 1인 로그 삭제
    delete_log_by_id(1)

    # 모든 로그 가져오기
    logs = get_logs()
    print(f"Total logs: {len(logs)}")

    # 특정 로그 수준 가져오기 (예: "ERROR")
    error_logs = get_logs_by_level("ERROR")
    print(f"Error logs: {len(error_logs)}")

    # 최근 7일의 로그 가져오기
    recent_logs = get_recent_logs(7)
    print(f"Recent logs: {len(recent_logs)}")

    # 1페이지에 5개의 로그 가져오기
    page_logs = get_logs_paginated(page=1, page_size=5)
    for log in page_logs:
        print(
            f"ID: {log.id}, Level: {log.log_level}, Message: {log.message}, Timestamp: {log.timestamp}, Source: {log.source}")