#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """ Getter method to fetch cities related to the state """
        var = models.storage.all()
        city_list = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if city[0] == 'City':
                city_list.append(var[key])
        for elements in city_list:
            if elements.state_id == self.id:
                result.append(elements)
        return result
