# models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# SQLAlchemy Base 객체 생성
Base = declarative_base()

# Stock 모델
class Corps(Base):
    __tablename__ = 'corps'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    daily_scores = relationship("DailyScores", back_populates="corps")

    def __repr__(self):
        return f"<Corp(code={self.code}, name={self.name})>"

# StockPrice 모델
class DailyScores(Base):
    __tablename__ = 'daily_scores'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    red = Column(Integer, nullable=True)


    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    corps_id = Column(Integer, ForeignKey('corps.id'), nullable=False)
    corps = relationship("Corps", back_populates="daily_scores")

    def __repr__(self):
        return (f"<StockPrice(date={self.date}, open_price={self.open_price}, "
                f"close_price={self.close_price}, high_price={self.high_price}, "
                f"low_price={self.low_price}, volume={self.volume})>")


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 로그 수준 (예: ERROR, WARNING, INFO)
    log_level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    # 로그 출처 (예: 모듈, 파일명 등)
    source = Column(String, nullable=True)

    def __repr__(self):
        return f"<Log(id={self.id}, log_level={self.log_level}, message={self.message}, timestamp={self.timestamp}, source={self.source})>"