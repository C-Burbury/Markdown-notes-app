from fastapi import FastAPI
from app.routers import auth, user, notes, tags, search
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(title="Markdown Notes App")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(notes.router)
app.include_router(tags.router)
app.include_router(search.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}