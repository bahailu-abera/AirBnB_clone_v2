#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from os import environ


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state', cascade='all, delete')

    else:
        @property
        def cities(self):
            from models import storage
            city_list = []
            all_cities = storage.all(City)

            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
