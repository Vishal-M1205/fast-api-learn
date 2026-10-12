from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

conn_url = URL.create(
    **{
        "drivername": "postgresql+psycopg",
        "username": "postgres",
        "password": "CG-vak123",
        "host": "localhost",
        "port": 5432,
        "database": "task_db",
    }
)

# * in the drivername : postgresql is the db dialect , means SQL DB's follow the basic SQL Query
# * But some changes between the DBMS - so mention the DBMS for supporting its syntax

engine = create_engine(url=conn_url)

print(engine)
#! we can only pass URL TO CONNECT THE DB, so use URL from sqlalchemy.engine which
#! constructs URL from dict

# * Engine manages the database connectivity and pool of connections


with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))

    #! connnection.execute() returns a CursorResult Object - it won't return the result
    #! it acts as a proxy for the database cursor , it won't load all the data into the memory

    # * data fetched using .all(), .fetchone(), .mappings()

    print(
        result.scalar()
    )  #! return the first row , discards rest of the data , return None if no row

"""
SQLAlchemy strictly requires SQL statements to be explicit, executable constructs rather than 
raw Python strings. Wrapping your query in text() accomplishes two things:

Safety and Compatibility: In SQLAlchemy 2.0 and newer, passing a plain string directly to connection.execute()
throws an error. text() explicitly flags the string as a SQL command.

Parameter Binding: It allows you to safely pass variables into your SQL using named parameters 
(e.g., text("SELECT * FROM users WHERE id = :user_id")), which protects your database from SQL injection attacks.
"""
