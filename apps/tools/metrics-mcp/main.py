from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import textstat

app = FastAPI(
    title="Metrics MCP",
    description="A tool for scoring text against various editorial and stylistic metrics.",
    version="0.1.0"
)

# --- Pydantic Models ---

class ScoreRequest(BaseModel):
    text: str

class ScoreResponse(BaseModel):
    flesch_reading_ease: float
    avg_sentence_length: float
    complex_words_pct: float
    # ... other metrics can be added here

class GateRequest(BaseModel):
    score: Dict
    targets: Dict

# --- Helper Functions ---

def calculate_complex_word_percentage(text: str) -> float:
    """Calculates the percentage of complex words (3+ syllables)."""
    total_words = textstat.lexicon_count(text)
    if total_words == 0:
        return 0.0
    complex_words = textstat.difficult_words(text)
    return (complex_words / total_words) * 100

# --- API Endpoints ---

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}

@app.post("/score", response_model=ScoreResponse)
async def score_text(request: ScoreRequest):
    """Scores a piece of text based on various metrics."""
    text = request.text

    # Set the text for textstat to work on
    textstat.set_lang("en_US")

    # Calculate metrics
    flesch = textstat.flesch_reading_ease(text)
    avg_sent_len = textstat.avg_sentence_length(text)
    complex_pct = calculate_complex_word_percentage(text)

    return ScoreResponse(
        flesch_reading_ease=flesch,
        avg_sentence_length=avg_sent_len,
        complex_words_pct=complex_pct
    )

@app.post("/gate")
async def gate_score(request: GateRequest):
    """(Placeholder) Checks a score against targets and returns a pass/fail verdict."""
    # Example logic:
    # score = request.score
    # targets = request.targets
    # passed = score.get('flesch_reading_ease', 0) >= targets.get('flesch', 60)
    # verdict = "pass" if passed else "fail"
    # notes = "Flesch score meets target." if passed else "Flesch score is below target."
    return {"verdict": "pass", "notes": "Placeholder response."}
