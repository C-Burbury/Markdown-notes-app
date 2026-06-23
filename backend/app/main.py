from fastapi import FastAPI
from app.routers import auth, user, notes
app = FastAPI(title="Markdown Notes App")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(notes.router)


@app.get("/health")
async def health():
    return {"status": "ok"}