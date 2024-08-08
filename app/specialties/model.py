import sqlalchemy as sql

from database import Base

class Specialty(Base):
    __tablename__ = 'specialties'
 
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(255), nullable=False, server_default='')
    name_ar = sql.Column(sql.String(255), nullable=False, server_default='')
    image = sql.Column(sql.String(length=100))