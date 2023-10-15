from databases import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String, Float, DATETIME, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Instruments(Base):
    __tablename__ = 'instruments'
    __table_args__ = {'schema': 'dxcore'}
    id = Column(Integer, primary_key=True)
    symbol = Column(String)


class ActivityLegs(Base):
    __tablename__ = 'activity_legs'
    __table_args__ = (
        PrimaryKeyConstraint('instrument_id'),
        {'schema': 'dxcore'}
    )

    quantity = Column(Float)
    activity_id = Column(Integer)
    instrument_id = Column(Integer, ForeignKey(Instruments.id))
    price = Column(Float)
    instruments = relationship(Instruments)


class Activities(Base):
    __tablename__ = 'activities'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {'schema': 'dxcore'}
    )
    id = Column(Integer, ForeignKey(ActivityLegs.activity_id), primary_key=True)
    account_id = Column(String)
    description = Column(String)
    activity_type = Column(String)
    created_time = Column(DATETIME)
    activity = relationship(ActivityLegs)


class Accounts(Base):
    __tablename__ = 'accounts'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {'schema': 'dxcore'}
    )
    id = Column(Integer, ForeignKey(Activities.account_id))
    owner_id = Column(Integer)
    account_id = Column(String, name='account_code')
    clearing_code = Column(String)
    activities = relationship(Activities)


class Principals(Base):
    __tablename__ = 'principals'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {'schema': 'dxcore'}
    )
    id = Column(Integer, ForeignKey(Accounts.owner_id), primary_key=True)
    up = Column(String, name='name')
    accounts = relationship(Accounts)


if __name__ == "__main__":
    session = SessionLocal()
    result = (
        session.query(
            Accounts.account_id,
            Activities.activity_type,
            Activities.created_time,
            Principals.up,
            Activities.description,
            Instruments.symbol,
            ActivityLegs.quantity
        )
        .order_by(Activities.created_time.desc())
        .limit(5)
        .all()
    )
    print(result)
