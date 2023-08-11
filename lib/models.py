from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref=backref("company"))
    devs = relationship("Dev", secondary="freebies", viewonly=True)

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value)
        freebie.company = self
        freebie.dev = dev
        return freebie

    @classmethod
    def oldest_company(cls, session):
        return session.scalars(select(cls).order_by(Company.founding_year)).first()

    def __repr__(self):
        return f"<Company {self.name}>"


class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", backref=backref("dev"))
    companies = relationship("Company", secondary="freebies", viewonly=True)

    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False

    def give_away(self, dev, freebie):
        if self.received_one(freebie.item_name):
            freebie.dev = dev

    def __repr__(self):
        return f"<Dev {self.name}>"


class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    company_id = Column(Integer, ForeignKey("companies.id"))
    dev_id = Column(Integer, ForeignKey("devs.id"))

    # company = relationship("Company", back_populates="freebies")
    # dev = relationship("Dev", back_populates="freebies")

    def print_details(self):
        print(f"{self.dev} owns a {self.item_name} from {self.company}")

    def __repr__(self):
        return f"<Freebie {self.item_name}>"
