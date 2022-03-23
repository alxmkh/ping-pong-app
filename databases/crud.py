from sqlalchemy.orm import Session

from . import models


def get_current_counter(db: Session):
    return db.query(models.Ping).first()


def increment_counter(db: Session):
    cur = get_current_counter(db)
    db.query(models.Ping).update({"ping_counter": cur.ping_counter + 1})
    db.commit()
    return db.query(models.Ping).first()


def insert_counter(db: Session):
    db_item = models.Ping(ping_counter=0)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def database_health_check(db: Session):
    return db.execute("SELECT 'OK'").first()
