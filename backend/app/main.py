from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine
from .models import Base
from .scraper import scrape_wikipedia
from .crud import (
    get_article_by_url,
    create_article,
    get_all_articles,
    create_quiz,
    get_quiz_by_article_id
)
from .dependencies import get_db
from .quiz_generator import generate_quiz

# =========================
# APP INIT
# =========================
app = FastAPI(
    title="Wiki Quiz API",
    version="1.0.0",
    description="Generate quizzes from Wikipedia articles using LLMs"
)

# =========================
# CORS (Frontend + GH Pages)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for assignment/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DB TABLES (SAFE ON START)
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"status": "Wiki Quiz API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# GENERATE QUIZ
# =========================
@app.post("/quiz/generate")
def generate_quiz_api(
    url: str,
    db: Session = Depends(get_db)
):
    if "wikipedia.org/wiki/" not in url:
        raise HTTPException(
            status_code=400,
            detail="Invalid Wikipedia URL"
        )

    # ---------- CACHE ----------
    cached_article = get_article_by_url(db, url)

    if cached_article:
        # Repair old rows with empty summary
        if not cached_article.summary or not cached_article.summary.strip():
            scraped = scrape_wikipedia(url)
            cached_article.summary = scraped["summary"]
            cached_article.sections = scraped["sections"]
            db.commit()
            db.refresh(cached_article)

        quiz_row = get_quiz_by_article_id(db, cached_article.id)

        if quiz_row and quiz_row.quiz:
            return {
                "id": cached_article.id,
                "url": cached_article.url,
                "title": cached_article.title,
                "summary": cached_article.summary,
                "quiz": quiz_row.quiz,
                "related_topics": quiz_row.related_topics,
                "cached": True
            }

        quiz, related_topics = generate_quiz(
            cached_article.title,
            cached_article.summary
        )

        create_quiz(db, cached_article.id, quiz, related_topics)

        return {
            "id": cached_article.id,
            "url": cached_article.url,
            "title": cached_article.title,
            "summary": cached_article.summary,
            "quiz": quiz,
            "related_topics": related_topics,
            "cached": False
        }

    # ---------- NEW ARTICLE ----------
    scraped = scrape_wikipedia(url)

    article = create_article(db, {
        "url": url,
        "title": scraped["title"],
        "summary": scraped["summary"],
        "sections": scraped["sections"],
        "raw_html": scraped["raw_html"]
    })

    quiz, related_topics = generate_quiz(
        article.title,
        article.summary
    )

    create_quiz(db, article.id, quiz, related_topics)

    return {
        "id": article.id,
        "url": article.url,
        "title": article.title,
        "summary": article.summary,
        "quiz": quiz,
        "related_topics": related_topics,
        "cached": False
    }

# =========================
# QUIZ HISTORY
# =========================
@app.get("/quiz/history")
def quiz_history(db: Session = Depends(get_db)):
    articles = get_all_articles(db)
    return [
        {
            "id": a.id,
            "title": a.title,
            "url": a.url,
            "created_at": a.created_at
        }
        for a in articles
    ]
