import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from database_manager import InMemoryDatabase

# Create the FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# Use the example database implementation
database = InMemoryDatabase()

templates = Jinja2Templates(directory="templates")


# Request model for adding text
class AddTextRequest(BaseModel):
    text: str


# Request model for searching similar texts
class SearchRequest(BaseModel):
    id: int
    threshold: float = 0.9


@app.get("/", response_class=HTMLResponse)
async def get_html_page():
    return templates.TemplateResponse('index.html')


# Endpoint to add text to the database
@app.post("/add_text/")
def add_text(request: AddTextRequest):
    text_id = database.add_text(request.text)
    return {"id": text_id}


# Endpoint to search for similar texts by distance (POST method)
@app.post("/search_similar_texts_by_distance/")
def search_similar_texts_by_distance(request: SearchRequest):
    try:
        results = database.search_similar_texts_by_distance(request.id, request.threshold)
        return results
    except IndexError:
        raise HTTPException(status_code=404, detail="Text with given ID not found")


# Endpoint to search for similar texts by exact words match (POST method)
@app.post("/search_similar_texts_by_exact_words_match/")
def search_similar_texts_by_exact_words_match(request: SearchRequest):
    try:
        results = database.search_similar_texts_by_exact_words_match(request.id, request.threshold)
        return results
    except IndexError:
        raise HTTPException(status_code=404, detail="Text with given ID not found")


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
