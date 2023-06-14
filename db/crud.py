from sqlalchemy.orm import Session
from db import models, schemas

def create_record(db: Session, record: schemas.Record):
    db_record = models.Record(serial = record.serial, incomming_time = record.incomming_time, fileName = record.fileName)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def read_user(db: Session):
    return db.query(models.Record.serial).distinct().all()