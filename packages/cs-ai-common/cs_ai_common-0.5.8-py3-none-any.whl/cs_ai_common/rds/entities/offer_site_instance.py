from sqlalchemy import Column, ForeignKey, Integer
from cs_ai_common.rds.entities.base import Base


class OfferSiteInstance(Base):
    __tablename__ = "offer_site_instances"

    id = Column(Integer(), primary_key=True)
    offer_instance_id = Column(Integer(), ForeignKey('offer_instances.id'))
    external_site_instance_id = Column(Integer(), ForeignKey('external_site_instances.id'))
