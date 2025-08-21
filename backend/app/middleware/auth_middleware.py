from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from ..config import settings

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    簡易的な認証チェック（開発用）
    本番環境では適切な認証システムを実装してください
    """
    try:
        # 開発用：Bearerトークンが"dev-token"の場合のみ許可
        if credentials.credentials == "dev-token":
            return {"user_id": "dev-user", "username": "developer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効な認証トークンです"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証に失敗しました"
        )
