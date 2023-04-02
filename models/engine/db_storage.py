#!/usr/bin/python3
"""
This Module defines a class to manage DataBase Storage for HBNB clone
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
    DataBase Storage abstraction Class
    """
    __engine = None
    __session = None

    def __init__(self):
        from models.base_model import Base

        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieves all object depending on cls name
        """
        from models.base_model import Base

        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for c in Base.__subclasses__():
                objs += self.__session.query(c).all()

        return {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in objs}

    def new(self, obj):
        """ Adds the new object to the Storage """
        self.__session.add(obj)

    def save(self):
        """ Saves all changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ Removes an Object from the session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Reloads all objects from the database """
        from models.base_model import BaseModel, Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review


        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_maker)
        self.__session = Session()

    def close(self):
        """ resets the session from the database """
        self.__session.close()
