import sqlalchemy as sql
from sqlalchemy.orm import relationship

from database import Base

class Setting(Base):
    __tablename__ = 'app_setting'
 
    key = sql.Column(sql.String(length=10), primary_key=True)
    category = sql.Column(sql.String(length=10))
    value = sql.Column(sql.String(length=255), nullable=False)
    last_modified = sql.Column(sql.DateTime)

   
