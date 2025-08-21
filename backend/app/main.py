from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from .routes import moderation
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
app.include_router(moderation.router, prefix="/api/moderation", tags=["moderation"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Carp Connect Moderation API"}

# Lambda関数用ハンドラー
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
