from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from cs_ai_common.rds.entities.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    confirmed_password = Column(Boolean(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(timezone.utc))
    number_of_ads = Column(Integer(), default=0)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    refresh_token = Column(String(), nullable=True)
    login_count = Column(Integer(), default=0)

    offers = relationship('Offer', back_populates='user')
    external_site_instances = relationship('ExternalSiteInstance', back_populates='user')
