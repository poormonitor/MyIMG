from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from . import Base
from uuid import uuid4


class User(Base):
    __tablename__ = "users"

    uid = Column(String(64), primary_key=True, index=True, default=str(uuid4()))
    passwd = Column(String(64))
    email = Column(String(64))
    admin = Column(Boolean, default=False)

    items = relationship("Pic", back_populates="owner")
