from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.word_schemas import WordResponse
from app.dependencies.llm import llm

from app.core.database import SessionLocal
from app.models.models import Word

def save_word_to_db(user_id: int, result: WordResponse):
    db = SessionLocal()

    new_word = Word(
        word=result.word,
        meaning=result.meaning,
        definition=result.definition,
        example=result.example,
        user_id=user_id
    )

    db.add(new_word)
    db.commit()
    db.refresh(new_word)

    db.close()

    return new_word

# Parser
parser = PydanticOutputParser(pydantic_object=WordResponse)

# Prompt
prompt = ChatPromptTemplate.from_template("""
You are a dictionary assistant.

Word: {word}

Rules:
1. Return valid JSON only
2. The example MUST contain the word wrapped like this: **{word}**
3. Do not change the word form

{format_instructions}
""")

# Chain
chain = prompt | llm | parser


def generate_word_details(word: str, user_id: int) -> WordResponse:
    result = chain.invoke({
        "word": word,
        "format_instructions": parser.get_format_instructions()
    })

    # Safety check
    if word in result.example and f"**{word}**" not in result.example:
        result.example = result.example.replace(word, f"**{word}**")

    # ✅ SAVE TO DB
    save_word_to_db(user_id, result)

    return result