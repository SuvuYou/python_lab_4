from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Target

engine = create_engine('mysql+pymysql://root:11111111@localhost:3306/pp_lab')

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# target1 = Target(target_id=3, age_group=25, intrest_group="entertaiment");
# target2 = Target(target_id=4, age_group=40, intrest_group="business");

# session.add_all([target1, target2])

# session.commit()
