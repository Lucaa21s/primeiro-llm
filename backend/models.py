from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True)

    password = Column(String)

    chats = relationship("Chat", back_populates="user")


class Chat(Base):

    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="chats")

    messages = relationship(
        "Message",
        back_populates="chat",
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    role = Column(String)

    content = Column(Text)

    chat_id = Column(Integer, ForeignKey("chats.id"))

    chat = relationship(
        "Chat",
        back_populates="messages",
    )
