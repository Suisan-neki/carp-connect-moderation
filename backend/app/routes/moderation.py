from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas.moderation import ModerationCheck, ModerationResult, ModerationHistory
from ..services.moderation_service import ModerationService
from ..middleware.auth_middleware import get_current_user

router = APIRouter()
moderation_service = ModerationService()

@router.post("/check", response_model=ModerationResult)
async def check_content(
    check_data: ModerationCheck,
    current_user = Depends(get_current_user)
):
    """
    コンテンツのモデレーションチェックを実行します。
    """
    try:
        result = await moderation_service.check_content(check_data.content, check_data.content_type)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"モデレーションチェック中にエラーが発生しました: {str(e)}"
        )

@router.get("/history", response_model=List[ModerationHistory])
async def get_moderation_history(
    current_user = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    """
    モデレーション履歴を取得します。
    """
    try:
        history = await moderation_service.get_moderation_history(limit, offset)
        return {"status": "success", "data": history}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"モデレーション履歴の取得中にエラーが発生しました: {str(e)}"
        )

@router.get("/stats")
async def get_moderation_stats(
    current_user = Depends(get_current_user)
):
    """
    モデレーション統計情報を取得します。
    """
    try:
        stats = await moderation_service.get_moderation_stats()
        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"モデレーション統計情報の取得中にエラーが発生しました: {str(e)}"
        )
