#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import (
    Table, Column, String, Integer, DateTime, ForeignKey, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import models
import os


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"), primary_key=True,
           nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False
        )
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete, delete-orphan"
        )

    if os.getenv('HBNB_TYPE_STORAGE') == 'fs':
        @property
        def reviews(self):
            """
            Returns the list of Review instances where place_id == Place.id
            """
            reviews_list = list()
            for review in models.storage.all(models.Review).values():
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """
            Returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place.
            """
            amenities_list = list()
            for amenity in models.storage.all(models.Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj=None):
            """
            Handles append method for adding an Amenity.id to the
            attribute amenity_ids.
            """
            if not isinstance(obj, models.Amenity):
                return
            self.amenities_ids.append(obj.id)
