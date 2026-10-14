#
#! Instead of writing queries , SQLAlchemy uses Python classes for representing the query
#! The class should represent the table and able to be mapped with the SQL
#! So for that we use declarative base
#! This doesn't create the table, it is just a representation

from sqlalchemy import String, ForeignKey, CheckConstraint, Index, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

#! use the DeclarativeBase to define the ORM and extract  mapped info from the python classes

convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s",
}

metadata = MetaData(schema="public", naming_convention=convention)
#! MAKESURE - the Base has the above metadata


class Base(DeclarativeBase):
    metadata = metadata
    pass


"""
Base.metadata.create_all(engine) - sqlalch use this to create all the tables from the base class
so instead using DeclarativeBase for evry model , use one inherited Base then it has all the table data
together
"""

#! MetaData - contains the details about table, constraint, schemas other db objects

#! Base.metadata.create_all(engine) - as Base is a DeclarativeClass , where all the ORM are
#! created from Base , so Base contains the structure of the table
#! accessed by its metadata

#! What if the table already exists - nothing happens , if the model has extra
#! column than the db table nothing happens


#! column_0_name means - we pass names in array for a composite key/ foreign key , so use the first name

# * conventions are automatically used and mapped by the MetaData based on the key , when created these
# ! format is used


class User(Base):
    __tablename__ = "users"  #! represents the table name
    """
    What is Mapped[] - a type annotation for SQLAl used for mapping ORM
    mapped_column() - config of the attrbute which reflect in as db column
    String - sqlal use its own datatype for Mapping to differ it from python datatype

    by default nullable = false , to make it true use anootaion  Mapped[str | None]
    so everythng is NOT NULL

    therfore annotations are imp and deliver meaning in orm maping
    """

    # * `__table_args__` is  used to define table level configurations, uses the column name and
    # * can create constraint all the constraint with name

    #! metadata = metadata - manual registertion , no need DeclarativeBase have one by default
    #! can register if new features need to be added

    metadata = metadata

    __table_args__ = (
        CheckConstraint(
            "age >= 18", name="cuser_age"
        ),  #! Even though it has name, it will be formatted
        Index("user_name", "name"),
        {"schema": "public"},
        #! Here "public" is the schema name tells which schema the table belongs
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    age: Mapped[int | None]

    tasks: Mapped[list["Tasks"]] = relationship(back_populates="user")

    #! id: Mapped[int] = mapped_column(primary_key=True)
    # * We don't need SERIAL in postgres because , new id is generated
    # * beecause of int-primary-key declaraton in sqlal


class Tasks(Base):
    __tablename__ = "tasks"

    metadata = metadata

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    #! If no String auto to VARCHAR()

    user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id"))

    user: Mapped["User"] = relationship(back_populates="tasks")

    #! This is how foreign keys are mapped , the "users" is the


# * to use composite primary key -> use primary_key = True in both columns

print(metadata.tables)


user = User(name="Vishal", email="v@gmail.com", age=20)

#! The above object is called ORM object - used by SQLAlchemy in a session , and process
#! the object as row

#! before knowing more about ORM Object - need to know session
#! Session is oject handles ORM Object - without Session, query to be written
#! as strings , session can use the ORM object to do db ops

"""
Engine: Manages database connectivity and the connection pool.
Connection: Provides access to a database connection.
Session: Manages ORM objects and coordinates their persistence to the database.
"""
"""
Session is created, as a contextmanager  it tracks all the changes made to a ORM object
and before commit all the changes are moved to database as a SQL ops and
it is commited - commit()

Identity Map - within a session , a object is stored with its primary key , for reusing
the same identity when it is called once again in the same session 

eg : 
user1  = session.get(User,1)
user2  = session.get(User,1)

both refers to the same object user1 is user2 = True

Transaction flow :
 session.commit() - commits the changes
 session.rollback() - rollbacks all the changes when a error is encountered

but opening a SessioLocal won't handle the transaction auto 

session.begin() - handles the commit/rollback 
can be used as SessionLocal.begin()

session.close() - handled by the SessioLocal context mangager automatically 
where it cleans the resource uses like connection, detach the object, 
rollback all the changes if not commited

"""


print(user)

"""
State of ORM Object 
Transient - creating as python object
Pending - means the object created as Transient moves into the session using add()
Persistent - happens when the object is repr as a database row and associated with the SqlAl happens
when the newly added Pending is flushed 
The Object is persistent when called from the db itself , the .get()
Detached - the object associated with session got disconnected - during commit()

but expire_on_commit is diff 
"""
