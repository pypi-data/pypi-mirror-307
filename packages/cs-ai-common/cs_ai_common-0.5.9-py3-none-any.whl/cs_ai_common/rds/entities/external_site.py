from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from cs_ai_common.rds.entities.base import Base


class ExternalSite(Base):
    __tablename__ = "external_site"

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False)
    logo_url = Column(String(200), nullable=False)
    base_url = Column(String(200), nullable=False)

    external_site_instances = relationship('ExternalSiteInstance', back_populates='external_site')