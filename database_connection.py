import os
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import Session

from custom_dataclasses import reg, Member, Group

from dotenv import load_dotenv

# connect to database using credentials from .env
# TODO: uncomment assignment
load_dotenv('.env')
sql_engine = sqlalchemy.create_engine(os.getenv("RDS_FULL"))
# sql_engine = None


# .connect(host=os.getenv("RDS_ENDPOINT"), db=os.getenv("RDS_DB_NAME"),
#                 user=os.getenv("RDS_USERNAME"), password=os.getenv("RDS_PASSWORD")))

def add_member(*, member: Member):
    with Session(sql_engine) as session:
        session.add(member)
        session.commit()


def add_group(*, group: Group):
    with Session(sql_engine) as session:
        session.add(group)
        session.commit()

def db_register(group: Group, by: Member):
    with Session(sql_engine) as session:
        session.add(by)
        group.members.append(by)
        session.add(group)
        session.commit()

# if __name__ == '__main__':
#     load_dotenv('.env')
#     sql_engine = sqlalchemy.create_engine(os.getenv("RDS_FULL"))
#     reg.metadata.drop_all(sql_engine)
#     reg.metadata.create_all(sql_engine)
#     # clear metadata
#
#     with Session(sql_engine) as session:
#         member = Member(username='XXXX', id=1)
#         session.add(member)
#         session.commit()
#     print("Done")
