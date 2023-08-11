#!/usr/bin/env python3

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Company, Dev, Freebie

if __name__ == "__main__":
    engine = create_engine("sqlite:///freebies.db", echo=True)
    session = Session(engine)
    import ipdb

    ipdb.set_trace()
    session.close()
