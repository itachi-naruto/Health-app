import sqlalchemy as sql
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = 'users'
 
    id = sql.Column(sql.Integer, primary_key=True)
    active = sql.Column('is_active', sql.Boolean(), nullable=False, server_default='1')

    phone = sql.Column(sql.Integer, nullable=False, unique=True)
    email = sql.Column(sql.String(255), nullable=False, unique=True)
    
    mobile_confirmed_at = sql.Column(sql.DateTime())
    email_confirmed_at = sql.Column(sql.DateTime())
    password = sql.Column(sql.String(255), nullable=False, server_default='')
    public_id = sql.Column(sql.String(length=255))
    otp = sql.Column(sql.String(length=6))
    expiration_time = sql.Column(sql.DateTime())
    has_profile = sql.Column(sql.Boolean(), nullable=False, server_default='0')

    # Define the relationship to Role via UserRoles
    roles = relationship('Role', secondary='user_roles')

    # Relationship to Patient
    patients = relationship('Patient', cascade="all, delete-orphan")

    # Relationship to Doctor
    doctors = relationship('Doctor', cascade="all, delete-orphan")

    # Relationship to Center
    centers = relationship('Center', cascade="all, delete-orphan")

    # Relationship to Tracking
    track = relationship('Tracking')

# Define the Role data-model
class Role(Base):
    __tablename__ = 'roles'
    id = sql.Column(sql.Integer(), primary_key=True)
    name = sql.Column(sql.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = sql.Column(sql.Integer(), primary_key=True)
    user_id = sql.Column(sql.Integer(), sql.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = sql.Column(sql.Integer(), sql.ForeignKey('roles.id', ondelete='CASCADE'))


class Tracking(Base):
    __tablename__ = 'login_tracking'
    id = sql.Column(sql.Integer(), primary_key=True)
    date = sql.Column(sql.DateTime())
    status = sql.Column(sql.String(length=255))
    others = sql.Column(sql.String(length=255), server_default=None)

    user_id = sql.Column(sql.Integer(), sql.ForeignKey('users.id', ondelete='CASCADE'))