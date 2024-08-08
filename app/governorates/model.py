import sqlalchemy as sql
from sqlalchemy.orm import relationship

from database import Base

class Governorate(Base):
    __tablename__ = 'governorates'
 
    id = sql.Column(sql.Integer, primary_key=True)

    # Governorate information
    g_name = sql.Column(sql.String(50), nullable=False, server_default='')
    main_wilayat = sql.Column(sql.String(50), nullable=False, server_default='')
    total_wilayat = sql.Column(sql.Integer, nullable=False)

    wilayats = relationship('Wilayat', back_populates='governorates', cascade="all, delete-orphan")

class Wilayat(Base):
    __tablename__ = 'wilayats'

    # Wilayat information
    
    id = sql.Column(sql.Integer, primary_key=True)
    w_name = sql.Column(sql.String(50), nullable=False, server_default='')
    g_id = sql.Column(sql.Integer(), sql.ForeignKey('governorates.id', ondelete='CASCADE'))

    governorates = relationship('Governorate', back_populates='wilayats')

    # doctors = relationship('Doctor',back_populates='wilayats', cascade="all, delete-orphan")