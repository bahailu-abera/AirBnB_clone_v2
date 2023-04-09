#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table

from sqlalchemy.orm import relationship


place_amenity = Table('association', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship('Review', backref='place', cascade='all, delete')
    amenities = relationship('Amenity', backref='places', viewonly=False,
                             secondary=place_amenity)


    @property
    def reviews(self):
        """ Getter method for reviews """
        from models import storage
        review_list = []
        for review in storage.all('Review').values():
            if review.place_id == self.id:
                review_list.append(review)

        return review_list

    @property
    def amenities(self):
        """ Getter method for amenities """
        from models import storage
        amenities_list = []
        for amenity in storage.all('Amenity').values():
            if amenity.place_id == self.id:
                amenities_list.append(amenity)

        return amenities_list

    @amenities.setter
    def amenities(self, object=None):
        """ Setter method for the amenity """
        if type(object).__name__ == "Amenity":
            self.amenity_ids.append(object)
