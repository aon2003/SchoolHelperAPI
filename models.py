import enum

import sqlalchemy.orm
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, \
    SmallInteger, Time, UniqueConstraint, BigInteger, Table, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from database import Base


# Table for MANY - TO - MANY relation for Teachers to Subjects of a Class
class_subject_teacher = Table(
    'class_subject_teacher', Base.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('class_subject_id', ForeignKey('class_subject.id')),
    Column('user_id', ForeignKey('user.id')),

    UniqueConstraint(
        'class_subject_id', 'user_id',
        name='class_subject_id_user_id_uc'
    )
)


# Table for MANY-TO-MANY relation for Classes to Subjects
# class ClassSubject(Base):
#     __tablename__ = 'class_subject'
#
#     id = Column(Integer, primary_key=True, index=True)
#     class_id = Column('class_id', ForeignKey('class.id'))
#     subject_id = Column('subject_id', ForeignKey('subject.id'))
#
#     UniqueConstraint('class_id', 'subject_id', name='class_id_subject_id_uc')

class_subject = Table(
    'class_subject', Base.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('class_id', ForeignKey('class.id')),
    Column('subject_id', ForeignKey('subject.id')),

    UniqueConstraint('class_id', 'subject_id', name='class_id_subject_id_uc'),
)


class Class(Base):
    __tablename__ = "class"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String(length=20), nullable=True, unique=True)
    name = Column(String(length=10), nullable=False, unique=True)
    key = Column(String(length=60), nullable=False, unique=True)
    
    subjects = relationship(
        "Subject",
        secondary=class_subject,
        back_populates="classes"
    )


class Subject(Base):
    __tablename__ = "subject"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False, unique=True)
    
    classes = relationship(
        "Class",
        secondary=class_subject,
        back_populates="subjects"
    )


# TODO
class GuildCategory(Base):
    __tablename__ = "guild_category"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String(length=20), nullable=False)
    category_id = Column(String(length=50), nullable=False)
    
    UniqueConstraint('guild_id', 'name', name='guild_id_name_uc')


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String(length=20), nullable=False)
    username = Column(String(length=50), nullable=False)
    email = Column(String(length=50), nullable=False)
    password = Column(String(length=50), nullable=False)
    first_name = Column(String(length=50), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    type = Column(
        ENUM('student', 'teacher', 'admin', name='user_type_enum'),
        nullable=False
    )
    
    # class_subjects = relationship(
    #     "class_subject",
    #     back_populates="users",
    # )
