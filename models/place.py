#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
import shlex
import models
from models.amenity import Amenity

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """ Returns list of reviews.id """
            all_reviews = models.storage.all(Review)
            place_reviews = []
            for review_ins in all_reviews.values():
                if review_ins.place_id == self.id:
                    place_reviews.append(review_ins)

            return place_reviews

        @property
        def amenities(self):
            """ Returns list of amenity ids """
            all_amenities = models.storage.all(Amenity)
            place_amenities = []
            for amenity_ins in all_amenities.values():
                if amenity_ins.place_id == self.id:
                    place_amenities.append(amenity_ins)

            return place_amenities

        @amenities.setter
        def amenities(self, amenity_obj):
            """ Appends amenity ids to the attribute """
            if isinstance(amenity_obj, models.Amenity):
                self.amenities.append(amenity_obj.id)
