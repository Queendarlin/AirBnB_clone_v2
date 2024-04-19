#!/usr/bin/python3
"""New engine storage for SQLAlchemy"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """DBStorage engine class"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine (self.__engine)"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name
        Return: A dictionary of __object
        """
        dictionary = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                dictionary[key] = obj
            else:
                class_list = [State, City, Review, Amenity, Place, User]
                for a_class in class_list:
                    query = self.__session.query(a_class)
                    for obj in query:
                        key = '{}.{}'.format(type(obj).__name__, obj.id)
                        dictionary[key] = obj
            return dictionary

    def new(self, obj):
        """Adds object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute
        (self.__session)"""
        self.__session.remove()
