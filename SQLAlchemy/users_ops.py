from sqlalchemy import create_engine, URL, select
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import Session, sessionmaker
from declarative_base import User, Base, Tasks

conn_url = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="CG-vak123",
    host="localhost",
    database="task_db",
    port=5432,
)


engine = create_engine(
    url=conn_url,
    poolclass=QueuePool,
    pool_size=3,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

Base.metadata.create_all(bind=engine)

#! SessionContext = Session(bind=engine) creates one Session with its own config if another Session need
#! to be created, need to repeat the config again
#! sessionmaker is a factory - where we can wrap the config and create many session from the factory

SessionContext = sessionmaker(bind=engine)


"""with SessionContext.begin() as session:
    user = User(name="Vishal", email="vish @gmail.com", age=21)

    session.add(user)  #! - adds single object
    # ! session.add_all(iterable) - adds all the object wrapped in a iterable
    #! Both adds are used to add a object to the session

    session.commit()"""


"""with SessionContext.begin() as session:
    user = session.get(User, 1)

    print(user.name)

    user.name = "Vikas" """

#! scalars() return the object , execute() return the text

with SessionContext.begin() as session:
    query = select(User.name, User.age).where(User.name == "Vikas")
    #! Instead of mentioning the attr , if just User is mentioned then it will give object
    #! if attr then values are returned

    print(session.execute(query).all())  #! get all the mentioned attr
    print(
        session.scalars(query).all()
    )  #! scalars get all the value of the first selected column
    print(session.scalar(query))  #! get the first column first row value
