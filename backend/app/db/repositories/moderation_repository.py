import boto3
import logging
from typing import List, Dict, Any
from ...config import settings

logger = logging.getLogger(__name__)

class ModerationRepository:
    def __init__(self):
        # モックモード（ローカル開発用）
        self.mock_mode = (
            settings.DEBUG
            or not settings.AWS_ACCESS_KEY_ID
            or not settings.AWS_SECRET_ACCESS_KEY
        )
        self._mock_records: List[Dict[str, Any]] = []

        if not self.mock_mode:
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            self.table = self.dynamodb.Table(settings.DYNAMODB_MODERATION_TABLE)
        else:
            self.dynamodb = None
            self.table = None

    async def create_moderation_record(self, record: Dict[str, Any]) -> bool:
        """
        モデレーション記録を作成します。
        """
        try:
            if self.mock_mode:
                self._mock_records.append(record)
                return True
            self.table.put_item(Item=record)
            return True
        except Exception as e:
            logger.error(f"モデレーション記録の作成中にエラーが発生しました: {str(e)}")
            return False

    async def get_moderation_history(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        モデレーション履歴を取得します。
        """
        try:
            if self.mock_mode:
                # offsetは単純なページングとして扱う
                start = offset
                end = offset + limit
                return list(reversed(self._mock_records))[start:end]
            response = self.table.scan(
                Limit=limit,
                ExclusiveStartKey={'moderation_id': str(offset)} if offset > 0 else None
            )
            return response.get('Items', [])
        except Exception as e:
            logger.error(f"モデレーション履歴の取得中にエラーが発生しました: {str(e)}")
            return []

    async def get_total_moderation_count(self) -> int:
        """
        総モデレーション数を取得します。
        """
        try:
            if self.mock_mode:
                return len(self._mock_records)
            response = self.table.scan(Select='COUNT')
            return response.get('Count', 0)
        except Exception as e:
            logger.error(f"総モデレーション数の取得中にエラーが発生しました: {str(e)}")
            return 0

    async def get_approved_moderation_count(self) -> int:
        """
        承認されたモデレーション数を取得します。
        """
        try:
            if self.mock_mode:
                return sum(1 for r in self._mock_records if r.get('moderation_result') == 'approved')
            response = self.table.scan(
                FilterExpression='moderation_result = :result',
                ExpressionAttributeValues={':result': 'approved'},
                Select='COUNT'
            )
            return response.get('Count', 0)
        except Exception as e:
            logger.error(f"承認されたモデレーション数の取得中にエラーが発生しました: {str(e)}")
            return 0

    async def get_rejected_moderation_count(self) -> int:
        """
        拒否されたモデレーション数を取得します。
        """
        try:
            if self.mock_mode:
                return sum(1 for r in self._mock_records if r.get('moderation_result') == 'rejected')
            response = self.table.scan(
                FilterExpression='moderation_result = :result',
                ExpressionAttributeValues={':result': 'rejected'},
                Select='COUNT'
            )
            return response.get('Count', 0)
        except Exception as e:
            logger.error(f"拒否されたモデレーション数の取得中にエラーが発生しました: {str(e)}")
            return 0
