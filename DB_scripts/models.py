from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# class Advertiser(Base):
#     __tablename__ = 'advertiser'

#     advertiser_id=Column(Integer, primary_key=True)
#     first_name=Column('first_name', String(32))
#     last_name=Column('last_name', String(32))
#     position=Column('position', String(32))
#     experience=Column('experience', Integer)

# class Advertising_campaign(Base):
#     __tablename__ = 'advertising_campaign'

#     campaign_id=Column(Integer, primary_key=True)
#     environment_id=Column('environment_id', Integer)
#     team_id=Column('team_id', Integer)
#     costumer_id=Column('costumer_id', Integer)
#     budget=Column('budget', Integer)    
#     start_date=Column('start_date', Date)   
#     end_date=Column('end_date', Date)   

# class Advertising_team(Base):
#     __tablename__ = 'advertising_team'

#     team_id=Column(Integer, primary_key=True)
#     advertiser_id=Column('advertiser_id', Integer)

# class Costumer(Base):
#     __tablename__ = 'costumer'

#     costumer_id=Column(Integer, primary_key=True)
#     first_name=Column('first_name', String(32))    
#     last_name=Column('last_name', String(32))    

# class Environment(Base):
#     __tablename__ = 'environment'

#     costumer_id=Column(Integer, primary_key=True)
#     target_id=Column('target_id', Integer)    
#     social_media=Column('social_media', String(32))    

# class Payment(Base):
#     __tablename__ = 'payment'

#     payment_id=Column(Integer, primary_key=True)
#     costumer_id=Column('costumer_id', Integer)    
#     campaign_id=Column('campaign_id', Integer)    
#     description=Column('description', String(255))    
#     amount=Column('amount', Integer)    
#     date=Column('date', Date)    

# class Target(Base):
#     __tablename__ = 'target'

#     target_id=Column(Integer, primary_key=True)
#     age_group=Column('age_group', Integer)    
#     intrest_group=Column('intrest_group', String(255))    
