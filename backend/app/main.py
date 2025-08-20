from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from .routes import auth, board, post, comment, moderation
from .config import settings

app = FastAPI(title="Carp Connect Moderation API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(board.router, prefix="/api/boards", tags=["boards"])
app.include_router(post.router, prefix="/api/posts", tags=["posts"])
app.include_router(comment.router, prefix="/api/comments", tags=["comments"])
app.include_router(moderation.router, prefix="/api/moderation", tags=["moderation"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Carp Connect Moderation API"}

# Lambda関数用ハンドラー
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
