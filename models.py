import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timedelta
import json



DB_USER= 'najlaaalshehri'
DB_NAME = 'restaurant'
database_path = 'postgres://nhpsreympdkozj:04d22108e5056851b660b66ad4cc49e8cd15f533f7f541421f018f1a2cd4b150@ec2-54-225-228-142.compute-1.amazonaws.com:5432/daobk8vk05rlqs'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#-----------------------------------------------------#
#                      Models                         #
#-----------------------------------------------------#

# Table
class Table(db.Model):  
  __tablename__ = 'table'

  id = Column(Integer, primary_key=True)
  chairs_num = Column(Integer)
  reservation= db.relationship('Reservation', lazy=True)

  def __init__(self, chairs_num ):
    self.chairs_num = chairs_num

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'chairs_num': self.chairs_num,
    }


# Reservation model
class Reservation(db.Model):  
  __tablename__ = 'reservation'

  id = Column(Integer, primary_key=True)
  account =Column(String , nullable=False )
  guest =Column(String , nullable=False )
  table_id = Column(Integer, db.ForeignKey('table.id', ondelete='CASCADE'), nullable=False)
  appointmentـTime = Column( db.DateTime , default=datetime.utcnow() + timedelta(days=1) ,nullable=False )

  def __init__(self, account , guest , table_id , appointmentـTime ):
    self.account = account
    self.guest = guest
    self.table_id = table_id
    self.appointmentـTime = appointmentـTime

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'account':self.account,
      'table_id': self.table_id,
      'guest': self.guest,
      'appointmentـTime':self.appointmentـTime
    }



# menu model
class Menu(db.Model):  
  __tablename__ = 'menu'

  id = Column(Integer, primary_key=True)
  dish_name = Column(String)
  category = Column(String)
  description = Column(String)
  price = Column(String)   #make it integer

  def __init__(self, dish_name, description, category, price ):
    self.dish_name = dish_name
    self.description= description
    self.category = category
    self.price =  price

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'dish_name': self.dish_name,
      'description': self.description,
      'category': self.category,
      'price': self.price
    }

#-----------------------------------------------------#
#                   defualt values                    #
#-----------------------------------------------------#
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    
    table = Table(
        chairs_num = 1
    )

    table.insert()

    table = Table(
        chairs_num = 2
    )

    table.insert()

    table = Table(
        chairs_num = 3
    )

    table.insert()

    table = Table(
        chairs_num = 4
    )

    table.insert()

    table = Table(
        chairs_num = 5
    )

    table.insert()

    table = Table(
        chairs_num = 6
    )

    table.insert()

    table = Table(
        chairs_num = 8
    )

    table.insert()


    reservation = Reservation(
    	  account='Najla@gmail.com', 
        guest='Najla',
        table_id= 1,
        appointmentـTime= "2021-08-02 00:28:42"

    )

    reservation.insert()

    reservation = Reservation(
        account='Guest@gmail.com', 
        guest='Guest 1',
        table_id= 2,
        appointmentـTime= "2021-08-02 00:28:42"

    )

    reservation.insert()
    

    reservation = Reservation(
        account='Sara@gmail.com', 
        guest='Sara',
        table_id= 3,
        appointmentـTime= "2021-08-03 00:28:42"

    )
    reservation.insert()


    reservation = Reservation(
        account='john@gmail.com', 
        guest='john',
        table_id= 3,
        appointmentـTime= "2021-08-04 00:28:42"

    )

    reservation.insert()

    menu = Menu(
        dish_name = 'Margherita Pizza',
        category = 'Pizza',
        description = "Tomato sauce, Mozzarella, Cantal cheese and oregano",
        price = '25$'
    )


    menu.insert()

    menu = Menu(
        dish_name = 'vegtables Pizza',
        category = 'Pizze',
        description = "Tomato sauce, Mozzarella, and olives",
        price = '30$'
    )


    menu.insert()

    menu = Menu(
        dish_name = 'Mango juice',
        category = 'Cold Drinks',
        description = "Fresh Mango juice",
        price = '11$'
    )


    menu.insert()

    menu = Menu(
        dish_name = 'Kale salad',
        category = 'Salad',
        description = "Fresh Kale salad",
        price = '20$'
    )


    menu.insert()

    menu = Menu(
        dish_name = 'Beef Burger',
        category = 'Main dishes',
        description = "Grilled Beef Burger with cheese",
        price = '30$'
    )


    menu.insert()

    menu = Menu(
        dish_name = 'Chicken Burger',
        category = 'Main dishes',
        description = "Crispy Chicken Burger with cheese",
        price = '33$'
    )


    menu.insert()

    menu = Menu(
        dish_name = 'Kabsa',
        category = 'Main dishes',
        description = "Rice and Chicken cooked as the Traditional Saudi way",
        price = '135$'
    )


    menu.insert()

    menu = Menu(
        dish_name = 'Pesto Pasta',
        category = 'Main dishes',
        description = "Pasta with pesto sauce, Mozzarella, and olives",
        price = '130$'
    )


    menu.insert()