import sqlalchemy as sql

from database import Base

class Schedule(Base):
    __tablename__ = 'schedules'
 
    id = sql.Column(sql.Integer, primary_key=True)
    date_time = sql.Column(sql.DateTime())
    period = sql.Column(sql.Integer)
    active = sql.Column(sql.Boolean(), nullable=False, server_default='1')

    doctor_id = sql.Column(sql.Integer(), sql.ForeignKey('doctors.id', ondelete='CASCADE'))
    center_id = sql.Column(sql.Integer(), sql.ForeignKey('centers.id', ondelete='CASCADE'))