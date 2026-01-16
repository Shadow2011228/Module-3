import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

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