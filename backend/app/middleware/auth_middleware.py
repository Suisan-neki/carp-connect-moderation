from typing import Optional
from fastapi import Header


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    # 簡易なデモ用。実運用ではJWT検証等を実装してください。
    return {"user_id": "demo-user"}