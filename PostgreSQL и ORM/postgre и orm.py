import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import faker
import random

engine = create_engine('postgresql+psycopg2://postgres:Zz050508@localhost/rebotica')

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    hp = Column(Integer, default=100)
    damage = Column(Integer, default=20)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

a = Session()

# hero = Users(id=123, name='Keks')
# a.add(hero)
# a.commit()

enemy = Users(id = 228, name = "Ponchic")
a.merge(enemy)
a.commit()

fake = faker.Faker('ru_RU')
for x in range(400):
    user_id = random.randint(1000, 9999)
    name = fake.first_name()
    obj = Users(id=user_id, name=name)
    a.merge(obj)
    a.commit()


data = a.query(Users).all() # В переменной data будет лежать список со всеми записями в виде объектов класса Users
print(data)
for row in data:
    print(row.id, row.name, row.hp, row.damage) # Взятие атрибутов записи таблицы Users от объекта класса
print('=========================')

# В переменной data будет лежать список с записями где id > 9000 в виде объектов класса Users
data = a.query(Users).filter(Users.id > 9000)
for row in data:
    print(row.id, row.name, row.hp, row.damage)
print('=========================')

# В переменной data будет лежать список с записями, где id между 9000 и 9100 в виде объектов класса Users
data = a.query(Users).filter(Users.id > 9000, Users.id < 9100)
for row in data:
    print(row.id, row.name, row.hp, row.damage)
print('=========================')

# Обновит данные по фильтру, 'name' - название столбца, 'Lee' - значение на которое поменяется
a.query(Users).filter(Users.id > 9000, Users.id < 9100).update({'name':'Lee'})
data = a.query(Users).filter(Users.id > 9000, Users.id < 9200)
for row in data:
    print(row.id, row.name, row.hp, row.damage)
print('=========================')

# Удалит данные по фильтру (от id 9000 до 9100)
a.query(Users).filter(Users.id > 9000, Users.id < 9100).delete()
data = a.query(Users).filter(Users.id > 9000, Users.id < 9200)
for row in data:
    print(row.id, row.name, row.hp, row.damage)
print('=========================')

a.query(Users).filter(Users.id > 2000).delete()
data = a.query(Users).all()
for row in data:
    print(row.id, row.name, row.hp, row.damage)
print('=========================')