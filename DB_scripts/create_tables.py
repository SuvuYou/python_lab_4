from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('mysql+pymysql://root:11111111@localhost:3306/online_courses_lab')

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
