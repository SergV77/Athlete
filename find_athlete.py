import os
import uuid
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
  __tablename__ = "user"
  id = sa.Column(sa.INTEGER, primary_key=True)
  first_name = sa.Column(sa.TEXT)
  last_name = sa.Column(sa.TEXT)
  gender = sa.Column(sa.TEXT)
  email = sa.Column(sa.TEXT)
  birthdate = sa.Column(sa.TEXT)
  height = sa.Column(sa.REAL)
  

class Athelete(Base):
  __tablename__ = "athelete"
  id = sa.Column(sa.INTEGER, primary_key=True)
  name = sa.Column(sa.TEXT)
  birthdate = sa.Column(sa.TEXT)
  height = sa.Column(sa.REAL)  

  
  
def connect_db():
  engine = sa.create_engine(DB_PATH)
  Base.metadata.create_all(engine)
  session = sessionmaker(engine)
  return session()


def find_user(user_id):
  session = connect_db()
  user = session.query(User).filter(User.id == user_id).first()
  session.close()
  return user


def find_by_height(user_height):
  session = connect_db()
  atheletes = session.query(Athelete).filter(Athelete.height > 0).all()
  session.close()

  candidate = atheletes[0]
  for athelete in atheletes:
    candidate_diff = abs(candidate.height - user_height)
    athelete_diff = abs(athelete.height - user_height)

    if athelete_diff < candidate_diff:
      candidate = athelete

  return candidate
  

def find_by_birthdate(user_birthdate):
  session = connect_db()
  atheletes = session.query(Athelete).all()
  session.close() 

  candidate = atheletes[0]
  for athelete in atheletes:
    candidate_diff = date_diff(candidate.birthdate, user_birthdate)
    athelete_diff = date_diff(athelete.birthdate, user_birthdate)
    if athelete_diff < candidate_diff:
      candidate = athelete
  return candidate

def date_diff(date_1, date_2):
    
    datetime_1 = datetime.strptime(date_1, "%Y-%m-%d")    
    datetime_2 = datetime.strptime(date_2, "%Y-%m-%d")    
    diff = abs(datetime_1 - datetime_2)    
    return diff  


def main():  
  
  user_id = int(input("Введите ID пользователя: "))    
  user = find_user(user_id)

  if user:
    athelet_height = find_by_height(user.height)
    athelet_birth = find_by_birthdate(user.birthdate)
    print("Ближайший по дате рождения атлет: {} - {}".format(athelet_birth.name, athelet_birth.birthdate))
    print("Ближайший по росту атлет: {} - {}".format(athelet_height.name, athelet_height.height))
  else:
    print("Пользователь с таким ID не найден")


if __name__ == '__main__':
  main()  

