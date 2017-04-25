#!/usr/bin/python

from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shelter(Base):
	__tablename__ = 'shelter'
	
	name = Column(String(20))
	address = Column(String(50))
	city = Column(String(20))
	state = Column(String(20))
	zipCode = Column(String(5))
	website = Column(String(50))
	id = Column(Integer, primary_key=True)
	
class Puppy(Base):
	__tablename__ = 'puppy'
	
	name = Column(String(20))
	dateofbirth = Column(String(20))
	gender = Column(String(20))
	weight = Column(String(20))
	picture = Column(String(20))
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)
	id = Column(Integer, primary_key=True)
	

engine = create_engine('sqlite:///restaurantnemu.db')
DBSession = sessionmaker(bind=engine)

session = DBSession()
shelter_ny = Shelter(name='dog_shelter_ny', address='assHole', city='NY', state='NYS', zipCode='23456', website='dogs.org', id=200)
session.add(shelter_ny)
session.commit()

dog1 = Puppy(name='wc', dateofbirth='20071223', gender='male', weight='23', picture='a.jpg', shelter=shelter_ny, id=1)
dog2 = Puppy(name='dh', dateofbirth='20070000', gender='male', weight='12', picture='b.jpg', shelter=shelter_ny, id=2)
dog3 = Puppy(name='lh', dateofbirth='20030000', gender='male', weight='10', picture='b.jpg', shelter=None, id=3)
session.add(dog1)
session.add(dog2)
session.add(dog3)

session.commit()

session.query(Shelter).all()
session.query(Puppy).all()

session.close()