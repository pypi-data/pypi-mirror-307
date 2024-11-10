from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from cs_ai_common.rds.entities.base import Base

class Offer(Base):
    __tablename__ = "offers"
    
    id = Column(Integer(), primary_key=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    generation = Column(String(50), nullable=False)
    production_year = Column(Integer(), nullable=False)
    engine_capacity = Column(Integer(), nullable=False)
    engine_power = Column(Integer(), nullable=False)
    mileage = Column(Integer(), nullable=False)
    transmission = Column(String(30), nullable=False)
    fuel_type = Column(String(30), nullable=False)
    thumbnails_folder_url = Column(String(200), nullable=False)
    price = Column(Integer(), nullable=False)
    price_currency = Column(String(20), nullable=False)
    price_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    location = Column(String(50), nullable=False)
    equipment = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    damaged = Column(Boolean(), nullable=False)
    imported = Column(Boolean(), nullable=False)
    vin = Column(String(100), nullable=False)
    registration_number = Column(String(100), nullable=False)
    first_registration_date = Column(DateTime(), nullable=False)
    number_of_doors = Column(Integer(), nullable=False)
    body_type = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)

    tachnical_details = Column(String(), nullable=False)
    equipment = Column(String(), nullable=False)
    history = Column(String(), nullable=False)
    buy_options = Column(String(), nullable=False)

    user = relationship('User', back_populates='offers')
    user_id = Column(Integer(), ForeignKey('users.id'))

    offer_instances = relationship('OfferInstance', back_populates='offer')
