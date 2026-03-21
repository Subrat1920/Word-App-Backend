from fastapi import APIRouter
from app.schemas.word_schemas import WordRequest, WordResponse
from app.services.word_service import generate_word_details

from app.core.database import SessionLocal
from app.models.models import Word

router = APIRouter()


# ✅ Existing API (NO CHANGE)
@router.post("/word", response_model=WordResponse)
def get_word_details(request: WordRequest):
    return generate_word_details(request.word, request.user_id)


# ✅ NEW API (ADD THIS BELOW)
@router.get("/words")
def get_words(user_id: int, filter_type: str = "mine"):
    db = SessionLocal()

    if filter_type == "mine":
        words = db.query(Word).filter(Word.user_id == user_id)

    elif filter_type == "other":
        words = db.query(Word).filter(Word.user_id != user_id)

    elif filter_type == "all":
        words = db.query(Word)

    else:
        return {"error": "Invalid filter"}

    words = words.order_by(Word.created_at.desc()).all()

    result = []
    for w in words:
        result.append({
            "word": w.word,
            "meaning": w.meaning,
            "definition": w.definition,
            "example": w.example,
            "user_id": w.user_id
        })

    db.close()
    return result