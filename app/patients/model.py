import sqlalchemy as sql
from sqlalchemy.orm import relationship

from database import Base

class Patient(Base):
    __tablename__ = 'patients'
 
    id = sql.Column(sql.Integer, primary_key=True)

    # Patient information
    first_name = sql.Column(sql.String(255), nullable=False, server_default='')
    last_name = sql.Column(sql.String(255), nullable=False, server_default='')
    civil_id = sql.Column(sql.String(10), nullable=False, server_default='')
    address = sql.Column(sql.String(300), nullable=True, server_default='')
    gender = sql.Column(sql.String(length=100))
    birth_date = sql.Column(sql.DateTime())
    blood_type = sql.Column(sql.String(length=100))
    country = sql.Column(sql.String(length=100), server_default='Oman')

    user_id = sql.Column(sql.Integer(), sql.ForeignKey('users.id', ondelete='CASCADE'))

    parent_id = sql.Column(sql.Integer, sql.ForeignKey('patients.id'))
    relation = sql.Column(sql.String(length=100), nullable=True, server_default='')

    dependents = relationship('Patient')