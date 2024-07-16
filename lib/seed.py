#!/usr/bin/env python3
from faker import Faker
import random 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Audition, Role

engine = create_engine('sqlite:///auditions.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def delete_records():
    session.query(Audition).delete()
    session.query(Role).delete()
    session.commit()

def create_auditions():
    auditions = []
    for i in range(50):
        audition = Audition(
          actor = fake.unique.name(),
          location = fake.address(),
          phone = fake.phone_number(),
          hired = False
        )
        auditions.append(audition)

    session.add_all(auditions)
    session.commit()
    return auditions

def create_roles():
    roles = []
    for i in range(10):
        role = Role(
          character_name = fake.unique.name(),
        )
        roles.append(role)

    session.add_all(roles)
    session.commit()
    return roles

def relate_one_to_many(auditions, roles):
    for audition in auditions:
        audition.role = random.choice(roles)

    session.add_all(auditions)
    session.commit()
    return auditions, roles

if __name__ == '__main__':
    
    auditions  = create_auditions()
    roles = create_roles()
    auditions, roles = relate_one_to_many(auditions, roles)