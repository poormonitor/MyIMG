from sqlalchemy import Column, Text, Boolean, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Pic(Base):
    __tablename__ = "pic"

    pid = Column(String(64), primary_key=True, index=True)
    indate= Column(DateTime, default=func.now())
    ip = Column(String(256))
    ext = Column(String(5), index=True)
    private = Column(Boolean, default=False)
    owner_id = Column(String(64), ForeignKey("users.uid"))

    owner = relationship("User", back_populates="items")