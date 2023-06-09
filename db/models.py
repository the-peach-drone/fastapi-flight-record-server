from sqlalchemy import Column, Integer, String
from db.database import Base

class Record(Base):
    __tablename__  = "flightCache"
    
    record_id      = Column(Integer, primary_key=True, autoincrement=True)
    serial         = Column(String(50),  nullable=False)
    incomming_time = Column(String(50),  nullable=False)
    fileName       = Column(String(50),  nullable=False)