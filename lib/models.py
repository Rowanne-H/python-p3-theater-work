from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///freebies.db')

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean, default=False)
    
    role_id = Column(Integer(), ForeignKey('roles.id'))

    def call_back(self):
        self.hired = True

    def __repr__(self):
        return f'<Audition {self.id}>'
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    character_name = Column(String())

    auditions = relationship('Audition', backref='role')
    actors = association_proxy('auditions', 'actor', 
                               creator=lambda ac: Audition(actor=ac))
    locations = association_proxy('auditions', 'location', 
                               creator=lambda lo: Audition(location=lo))
    

    def lead(self):
        for audition in self.auditions:
            if audition.hired == True:
                return audition
        return 'no actor has been hired for this role'
    
    def understudy(self):
        num = 0
        for audition in self.auditions:
            if audition.hired == True:
                num+=1
                if num==2:
                    return audition
        return  'no actor has been hired for understudy for this role'
        

    def __repr__(self):
        return f'<Role {self.id}>'
    
    
