from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

from databases import Database
database = Database('postgres://username:password@db:5432/database')

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/plaintext_example", response_class=PlainTextResponse)
def main():
    return "Hello World"

@app.get("/highscores")
async def highscores_get():
    query = "SELECT * FROM HighScores"
    rows = await database.fetch_all(query=query)
    return rows

@app.post("/highscores")
async def highscores_post(request: Request):
    content = await request.json()
    query = "INSERT INTO HighScores(name, score) VALUES (:name, :score)"
    values = {"name": content["name"], "score": int(content["score"])}
    result = await database.execute(query=query, values=values)
    return result

@app.get("/highscores/{item_id}")
async def highscores_get_item(item_id: int):
    query = "SELECT * FROM HighScores WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": item_id})
    return result

@app.delete("/highscores/{item_id}")
async def highscores_delete_item(item_id: int):
    query = "DELETE FROM HighScores WHERE id = :id"
    result = await database.execute(query=query, values={"id": item_id})
    return result

@app.on_event("startup")
async def startup_event():
    await database.connect()

    query = """CREATE TABLE if not exists HighScores (id SERIAL, name VARCHAR(100), score INTEGER)"""
    await database.execute(query=query)
