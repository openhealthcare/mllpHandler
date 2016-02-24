import datetime
from contextlib import contextmanager

from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Boolean, ForeignKey
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///mllpHandler.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.



def get_plural_name(cls):
    return "{}s".format(cls.__tablename__)


@as_declarative()
class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)
    updated = Column(DateTime, onupdate=datetime.datetime.utcnow)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class GlossSubrecord(object):
    @declared_attr
    def gloss_reference_id(cls):
        return Column(Integer, ForeignKey('glossolaliareference.id'))

    @declared_attr
    def gloss_reference(cls):
        return relationship(
            "GlossolaliaReference",
            back_populates=get_plural_name(cls)
        )


class Patient(Base, GlossSubrecord):
    id = Column(Integer, primary_key=True)
    surname = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    middle_name = Column(String(250))
    title = Column(String(250))
    date_of_birth = Column(Date, nullable=False)
    sex = Column(String(250))
    marital_status = Column(String(250))
    religion = Column(String(250))
    date_of_death = Column(Date)

    # I know it seems like we can calculate this from the above
    # however it comes as a seperate field in the feed and
    # therefore might be useful for data validation purposes
    # (also might give us an indicator and the max time of death)
    death = Column(Boolean, default=False)
    birth_place = Column(String)


class PatientIdentifier(Base, GlossSubrecord):
    id = Column(Integer, primary_key=True)
    identifier = Column(String(250))
    issuing_source = Column(String(250))
    active = Column(Boolean, default=True)


class Subscription(Base, GlossSubrecord):
    id = Column(Integer, primary_key=True)
    system = Column(String(250))
    active = Column(Boolean, default=True)


class Admission(Base):
    admission = Column(DateTime)


class GlossolaliaReference(Base):
    id = Column(Integer, primary_key=True)

for subrecord in GlossSubrecord.__subclasses__():
    r = relationship(subrecord.__name__, back_populates="gloss_reference")
    setattr(GlossolaliaReference, get_plural_name(subrecord), r)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def __is_connected(hospital_number, issuing_source, session):
    return session.query(Subscription, GlossolaliaReference, PatientIdentifier).\
    filter(Subscription.gloss_reference_id == GlossolaliaReference.id).\
    filter(PatientIdentifier.gloss_reference_id == GlossolaliaReference.id).\
    filter(PatientIdentifier.issuing_source == issuing_source).\
    filter(PatientIdentifier.identifier == hospital_number)


# we need to get subscription from hospital number
def is_subscribed(hospital_number, issuing_source="uclh", session=None):
    is_connected = __is_connected(hospital_number, issuing_source, session)
    return is_connected.filter(Subscription.active == True).count()


def is_known(hospital_number, issuing_source="uclh", session=None):
    is_connected = __is_connected(hospital_number, issuing_source, session)
    return is_connected.count()