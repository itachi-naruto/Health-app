import sqlalchemy as sql

from database import Base

class Status(Base):
    __tablename__ = 'status'
 
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(255))
    name_ar = sql.Column(sql.String(255))
    # type = case or appointment 
    type = sql.Column(sql.String(255))