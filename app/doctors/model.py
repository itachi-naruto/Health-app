import uuid
from flask import g
import sqlalchemy as sql
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from database import Base

class Doctor(Base):
    __tablename__ = 'doctors'
 
    id = sql.Column(sql.Integer, primary_key=True)
    approved = sql.Column('is_approved', sql.Boolean(), nullable=False, server_default='0')

    # Doctor information
    first_name = sql.Column(sql.String(255), nullable=False, server_default='')
    last_name = sql.Column(sql.String(255), nullable=False, server_default='')
    gender = sql.Column(sql.String(length=100))
    birth_date = sql.Column(sql.DateTime())
    blood_type = sql.Column(sql.String(length=100))
    country = sql.Column(sql.String(length=100), server_default='Oman')
    address = sql.Column(sql.String(length=500))
    place_location = sql.Column(sql.String(length=100))
    exact_location = sql.Column(sql.String(length=100))
    speciality = sql.Column(sql.JSON)
    professional_experiance = sql.Column(sql.String(length=100))
    certification = sql.Column(sql.JSON)
    experiance = sql.Column(sql.String(length=100))
    education = sql.Column(sql.JSON)
    memberships = sql.Column(sql.JSON)
    follow_up_fee = sql.Column(sql.Numeric(10,3))
    consultation_fee = sql.Column(sql.Numeric(10,3))
    biography = sql.Column(sql.String(length=255))
    medical_board_registrations = sql.Column(sql.JSON)
    know_languages = sql.Column(sql.JSON)
    image = sql.Column(sql.String(length=100))
    contract_sign = sql.Column(sql.Boolean(), nullable=False, server_default='0')
    notes = sql.Column(sql.String(length=1000))

    history = relationship("DoctorHistory", backref="doctors", cascade="all, delete-orphan")

    user_id = sql.Column(sql.Integer(), sql.ForeignKey('users.id', ondelete='CASCADE'))

    # Relationship to Schedule
    schedule = relationship('Schedule')

    # Define the relationship to Center via CenetrDoctors
    center = relationship('Center', secondary='center_doctors')

    """
    def to_short_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'speciality': self.speciality,
            'image': self.image,
            'center': self.center[0].to_json() if self.center else None
        }
    """


# @listens_for(Doctor, 'before_insert')
# def before_insert_function(mapper, connection, target):
#     history_record = DoctorHistory(
#         doctor_id=target.id,
#         user_id=g.user.id,
#         username=g.user.phone,
#         action="insert",
#         field_name="all",
#         old_value="",
#         new_value="",
#     )
#     target.history.append(history_record)
    
@listens_for(Doctor, 'before_update')
def before_update_function(mapper, connection, target):
    state = sql.inspect(target)
    changes = {}

    for attr in state.attrs:
        history = attr.load_history()
        if history.has_changes():
            old_value = history.deleted[0] if history.deleted else None
            new_value = history.added[0] if history.added else None
            changes[attr.key] = (old_value, new_value)

    for field_name, (old_value, new_value) in changes.items():
        history_record = DoctorHistory(
            doctor_id=target.id,
            user_id=g.user.id,
            username=g.user.phone,
            action="update",
            field_name=field_name,
            old_value=str(old_value),
            new_value=str(new_value),
        )
        target.history.append(history_record)

class DoctorHistory(Base):
    __tablename__ = 'doctor_history'

    id = sql.Column(sql.Integer, primary_key=True)
    doctor_id = sql.Column(sql.Integer, sql.ForeignKey('doctors.id', name='fk_doctor_history_doctor_id_doctors'))
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', name='fk_doctor_history_user_id_users'))
    username = sql.Column(sql.String(length=255))
    action = sql.Column(sql.String(length=255))
    action_timestamp = sql.Column(sql.DateTime(), server_default=sql.func.now())
    field_name = sql.Column(sql.String(length=255))
    old_value = sql.Column(sql.String(length=255))
    new_value = sql.Column(sql.String(length=255))

    def to_json(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'action_timestamp': self.action_timestamp,
            'field_name': self.field_name,
            'old_value': self.old_value,
            'new_value': self.new_value
        }
