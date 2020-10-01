import os
import uuid
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Users(Base):
  __tablename__ = "user"
  id = sa.Column(sa.INTEGER, primary_key=True)
  first_name = sa.Column(sa.TEXT)
  last_name = sa.Column(sa.TEXT)
  gender = sa.Column(sa.TEXT)
  email = sa.Column(sa.TEXT)
  birthdate = sa.Column(sa.TEXT)
  height = sa.Column(sa.REAL)

  
def connect_db():
  engine = sa.create_engine(DB_PATH)
  Base.metadata.create_all(engine)
  session = sessionmaker(engine)
  return session()

def request_data():
  print("Привет! Я запишу твои данные!")
  first_name = input("Введи своё имя: ")
  last_name = input("Введите свою фамилию: ")
  gender = input("Введите свой пол: ")
  email = input("Введите адрес своей электронной почты: ")
  birthdate = input("Введите свою дату рождения: ")
  height = input("Введите свой рост: ")
  user_id = str(uuid.uuid4())
  user = Users(    
    first_name = first_name,
    last_name = last_name,
    gender = gender,
    email = email,
    birthdate = birthdate,
    height = height
  )
  return user

def find(name, session):
  query = session.query(Users).filter(Users.first_name == name)
  users_cnt = query.count()
  user_ids = [user.id for user in query.all()]
  return (users_cnt, user_ids)

def print_users_list(cnt, user_id):
  if user_id:
    print("Найдено пользователей: ", cnt)
  else:
    print("Пользователей с таким именем нет.")  



def main():  
  
  session = connect_db() 
  mode = input("Выбери режим.\n1 - найти пользователя по имени\n2 - ввести данные нового пользователя\n")  
  if mode == "1":    
    name = input("Введи имя пользователя для поиска: ")
    users_cnt, user_id = find(name, session)
    print_users_list(users_cnt, user_id)
    if user_id:
      print("Найден пользователь с идентификатором: ", user_id)      
    else:
      print("Такого пользователя нет.")
  elif mode == "2":
    user = request_data()   
    session.add(user)
    session.commit()        
    print("Спасибо, данные сохранены!")
  else:
    print("Некорректный режим:(")
  session.close()

if __name__ == '__main__':
  main()  

