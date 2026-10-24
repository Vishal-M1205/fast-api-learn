from declarative_base import User, Base, Tasks, metadata
from sqlalchemy import String, create_engine, URL, select, update, ForeignKey, Integer
from sqlalchemy.orm import Session, sessionmaker, Mapped, relationship, mapped_column
from users_ops import engine, SessionContext

"""
The relationship() works with the foreign key in the child table , back_populates creates
a bi-directional relation , while we can use just a relationship() in the child table ,
which create a unidirectional relationship. (many to one)

Course:
id 
name

Student
id
name
course_id -> Foreign key
course : Mapped["Course"] = relationship()

we can just pass the course object to the Student 
"""

"""
One to one relationship 

the one to one in sql is made with unique constraint to the foreign key 
where only one record from the parent is related to the child 

same like one to many user - tasks , tasks is list remove the list , just task
in the task model use unique to the foreign key of the user 
"""


class PostTagAssociation(Base):
    __tablename__ = "post_tag_associate"

    metadata = metadata

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)

    #! A table can have only on primary key - here two of them are primary key
    #! orm makes it as composite automatically PRIMARY KEY (posts.id,tags.id)


class Post(Base):
    __tablename__ = "posts"

    metadata = metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    tags: Mapped[list["Tag"]] = relationship(
        secondary="post_tag_associate", back_populates="posts"
    )


class Tag(Base):
    __tablename__ = "tags"

    metadata = metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    posts: Mapped[list["Post"]] = relationship(
        secondary="post_tag_associate", back_populates="tags"
    )


Base.metadata.create_all(bind=engine)

with SessionContext.begin() as session:
    post = Post(name="Good Morning")
    tag = Tag(name="DMK")

    post.tags.append(tag)

    #! tag.posts.append(post) - as we use backpropagates tag.posts is appended automatically
    #! so either append in tags or posts

    session.add_all([post, tag])

"""
The above example is for the many to many relation , as we cannot 
declare foreign key in both parent and table, we need third table (associate)
which has the foreign key of both the table , 
now in the relationship we pass the associate #!table name as 'secondary'
"""
