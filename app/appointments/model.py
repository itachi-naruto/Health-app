import sqlalchemy as sql

from sqlalchemy import UniqueConstraint
from database import Base

class Appointment(Base):
    __tablename__ = 'appointments'
 
    id = sql.Column(sql.Integer, primary_key=True)
    date = sql.Column(sql.DateTime())
    update_date = sql.Column(sql.DateTime())
    period = sql.Column(sql.Integer)

    doctor_id = sql.Column(sql.Integer(), sql.ForeignKey('doctors.id'))
    center_id = sql.Column(sql.Integer(), sql.ForeignKey('centers.id'))
    patient_id = sql.Column(sql.Integer(), sql.ForeignKey('patients.id'))
    #case_id = sql.Column(sql.Integer(), sql.ForeignKey('cases.id'))
    status_id = sql.Column(sql.Integer(), sql.ForeignKey('status.id'))

    payment_id = sql.Column(sql.String(length=255), server_default=None)

    slot_id = sql.Column(sql.Integer, server_default=None)

    symptoms = sql.Column(sql.String(length=512))

    __table_args__ = (
        UniqueConstraint('update_date', 'doctor_id', name='unique_doctor_time'),
    )