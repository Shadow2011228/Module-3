import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:Zz050508@localhost/rebotica')
Base = declarative_base()

class Users(Base):
    __tablename__ = 'Оценки'
    id = Column(Integer, primary_key=True, nullable=False)
    Evaluation = Column(Integer, nullable=False)
    Subject = Column(String, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

a = Session()

enemy = Users(id = 1, Evaluation = 5, Subject="Математика")
a.merge(enemy)
a.commit()

enemy = Users(id = 2, Evaluation = 5, Subject="Русский язык")
a.merge(enemy)
a.commit()