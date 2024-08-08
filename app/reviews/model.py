import sqlalchemy as sql

from database import Base

class Review(Base):
    __tablename__ = 'reviews'
 
    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(255))
    description = sql.Column(sql.String(1000))

    doctor_review = sql.Column(sql.Integer)
    center_review = sql.Column(sql.Integer)
    patient_review = sql.Column(sql.Integer)

    reviewed = sql.Column('is_reviewed', sql.Boolean(), nullable=False, server_default='0')
    
    reply_to = sql.Column(sql.Integer)

    review_date = sql.Column(sql.DateTime())

    reviewer_id = sql.Column(sql.Integer(), sql.ForeignKey('users.id'))
    doctor_id = sql.Column(sql.Integer(), sql.ForeignKey('doctors.id'))
    center_id = sql.Column(sql.Integer(), sql.ForeignKey('centers.id'))
    patient_id = sql.Column(sql.Integer(), sql.ForeignKey('patients.id'))