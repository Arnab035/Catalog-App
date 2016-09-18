from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250))

	@property
	def serialize(self):
		

		return{
			'name' : self.name,
			'email' : self.email,
			'id' : self.id
		}

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return{
			'name' : self.name,
			'category id' : self.id,
			'user-id' : self.user_id
			}



class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	description = Column(String(250))
	picture = Column(String(250))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return{
			'name' : self.name,
			'description' : self.description,
			'picture' : self.picture,
			'category-id' : self.category_id,
			'user-id' : self.user_id 
		}

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)