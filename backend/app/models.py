from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    sections = Column(JSON, default=list)
    raw_html = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(
        Integer,
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False
    )
    quiz = Column(JSON, nullable=False)
    related_topics = Column(JSON, default=list)
    created_at = Column(DateTime, server_default=func.now())
