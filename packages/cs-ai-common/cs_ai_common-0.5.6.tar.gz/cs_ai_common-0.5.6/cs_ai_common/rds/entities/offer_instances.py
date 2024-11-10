from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from cs_ai_common.rds.entities.base import Base


class OfferInstance(Base):
    __tablename__ = "offer_instances"

    id = Column(Integer(), primary_key=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(timezone.utc))
    external_url = Column(String(50), nullable=False)
    views = Column(Integer(), default=0)
    offer_id = Column(Integer(), ForeignKey('offers.id'))

    offer = relationship('Offer', back_populates='offer_instances')