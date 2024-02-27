import sqlalchemy
import os

# connect to database using credentials from .env
sql_engine = sqlalchemy.create_engine(os.getenv("RDS_FULL"))


# .connect(host=os.getenv("RDS_ENDPOINT"), db=os.getenv("RDS_DB_NAME"),
#                 user=os.getenv("RDS_USERNAME"), password=os.getenv("RDS_PASSWORD")))

def __main__():
    pass
