from cs_ai_common.rds.entities.offer_instances import OfferInstance
from cs_ai_common.rds.entities.offer_site_instance import OfferSiteInstance
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from cs_ai_common.rds.entities.base import Base


class ExternalSiteInstance(Base):
    __tablename__ = "external_site_instances"

    id = Column(Integer(), primary_key=True)
    auth_type = Column(String(50), nullable=False)
    auth_creds = Column(String(200), nullable=False)

    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship('User', back_populates='external_site_instances')
    
    external_site_id = Column(Integer(), ForeignKey('external_site.id'))
    external_site = relationship('ExternalSite', back_populates='external_site_instances')

    offer_instances = relationship(OfferInstance, secondary=OfferSiteInstance, back_populates='external_site_instances')
