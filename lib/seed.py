#!/usr/bin/env python3

# Script goes here!

from models import Company, Dev, Freebie
import random
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session
from faker import Faker


engine = create_engine("sqlite:///freebies.db", echo=True)

fake = Faker()


def create_data(session):
    companies = []
    devs = []
    freebies = []
    for i in range(20):
        companies.append(
            Company(name=fake.company(), founding_year=random.randint(1950, 2023))
        )
        devs.append(Dev(name=fake.name()))
    session.add_all(companies + devs)
    session.commit()
    for company in companies:
        # for each comapany create multiple freebies and give each on to a dev:
        for i in range(5):
            freebie = Freebie(item_name=fake.word(), value=random.randint(1, 50))
            freebie.company = company
            freebie.dev = random.choice(devs)
            freebies.append(freebie)
    session.add_all(freebies)
    session.commit()
    return companies, devs, freebies


def delete_data(session):
    session.execute(delete(Company))
    session.execute(delete(Dev))
    session.execute(delete(Freebie))


with Session(engine) as session:
    delete_data(session)
    companies, devs, freebies = create_data(session)
