from sqlalchemy.orm import Session
from .models import Article, Quiz


def get_article_by_url(db: Session, url: str):
    return db.query(Article).filter(Article.url == url).first()


def create_article(db: Session, data: dict):
    article = Article(**data)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_quiz_by_article_id(db: Session, article_id: int):
    return db.query(Quiz).filter(Quiz.article_id == article_id).first()


def create_quiz(db: Session, article_id: int, quiz: list, related_topics: list):
    q = Quiz(
        article_id=article_id,
        quiz=quiz,
        related_topics=related_topics
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def get_all_articles(db: Session):
    return db.query(Article).order_by(Article.created_at.desc()).all()
