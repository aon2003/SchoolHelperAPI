from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Class(Base):
    __tablename__ = "class"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String(length=20), nullable=True, unique=True)
    name = Column(String(length=10), nullable=False, unique=True)
    key = Column(String(length=60), nullable=False, unique=True)
    
    class_teacher = relationship(
        "User",
        back_populates="class_",
        uselist=False
    )
    
    subjects = relationship(
        "Subject",
        secondary='class_subject',
        back_populates="classes"
    )


class Subject(Base):
    __tablename__ = "subject"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False, unique=True)
    
    classes = relationship(
        "Class",
        secondary='class_subject',
        back_populates="subjects"
    )


class ClassSubject(Base):
    __tablename__ = "class_subject"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(ForeignKey('class.id'))
    subject_id = Column(ForeignKey('subject.id'))
    user_id = Column(ForeignKey('user.id'))
    
    class_ = relationship('Class', backref="class_subjects")
    subject = relationship('Subject', backref="class_subjects")
    teacher = relationship('User')


# TODO Maybe obsolete
# class GuildCategory(Base):
#     __tablename__ = "guild_category"
#
#     id = Column(Integer, primary_key=True, index=True)
#     guild_id = Column(String(length=20), nullable=False)
#     category_id = Column(String(length=50), nullable=False)
#
#     UniqueConstraint('guild_id', 'name', name='guild_id_name_uc')


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=50), nullable=False, unique=True)
    password = Column(String(length=60), nullable=False)
    first_name = Column(String(length=50), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    admin = Column(Boolean, nullable=False, default=False)
    class_id = Column(ForeignKey('class.id'), nullable=True, unique=True)

    class_ = relationship("Class", back_populates="class_teacher",
                          uselist=False)

    # class_subjects = relationship(
    #     "class_subject",
    #     back_populates="users",
    # )
