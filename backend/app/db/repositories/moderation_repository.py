import boto3
import time
from typing import List, Dict, Any
from ..dynamodb import get_dynamodb_client
from ...config import settings

class ModerationRepository:
    def __init__(self):
        self.dynamodb = get_dynamodb_client()
        self.table_name = settings.DYNAMODB_MODERATION_TABLE

    async def create_moderation_record(self, moderation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        モデレーション記録を作成します。
        """
        try:
            self.dynamodb.put_item(
                TableName=self.table_name,
                Item={
                    "moderation_id": {"S": moderation_data["moderation_id"]},
                    "content_id": {"S": moderation_data["content_id"]},
                    "content_type": {"S": moderation_data["content_type"]},
                    "original_content": {"S": moderation_data["original_content"]},
                    "moderation_result": {"S": moderation_data["moderation_result"]},
                    "moderation_reason": {"S": moderation_data["moderation_reason"]},
                    "moderation_score": {"N": str(moderation_data["moderation_score"])},
                    "created_at": {"N": str(moderation_data["created_at"])}
                }
            )
            return moderation_data
        except Exception as e:
            print(f"モデレーション記録の作成中にエラーが発生しました: {str(e)}")
            raise

    async def get_moderation_history(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        モデレーション履歴を取得します。
        """
        try:
            response = self.dynamodb.scan(
                TableName=self.table_name,
                Limit=limit
            )
            
            items = response.get("Items", [])
            result = []
            
            for item in items:
                result.append({
                    "moderation_id": item["moderation_id"]["S"],
                    "content_id": item["content_id"]["S"],
                    "content_type": item["content_type"]["S"],
                    "original_content": item["original_content"]["S"],
                    "moderation_result": item["moderation_result"]["S"],
                    "moderation_reason": item["moderation_reason"]["S"],
                    "moderation_score": float(item["moderation_score"]["N"]),
                    "created_at": int(item["created_at"]["N"])
                })
            
            return result
        except Exception as e:
            print(f"モデレーション履歴の取得中にエラーが発生しました: {str(e)}")
            raise

    async def get_total_moderation_count(self) -> int:
        """
        モデレーションの総数を取得します。
        """
        try:
            response = self.dynamodb.scan(
                TableName=self.table_name,
                Select="COUNT"
            )
            return response.get("Count", 0)
        except Exception as e:
            print(f"モデレーション総数の取得中にエラーが発生しました: {str(e)}")
            raise

    async def get_approved_moderation_count(self) -> int:
        """
        承認されたモデレーションの数を取得します。
        """
        try:
            response = self.dynamodb.scan(
                TableName=self.table_name,
                FilterExpression="moderation_result = :result",
                ExpressionAttributeValues={
                    ":result": {"S": "approved"}
                },
                Select="COUNT"
            )
            return response.get("Count", 0)
        except Exception as e:
            print(f"承認モデレーション数の取得中にエラーが発生しました: {str(e)}")
            raise

    async def get_rejected_moderation_count(self) -> int:
        """
        拒否されたモデレーションの数を取得します。
        """
        try:
            response = self.dynamodb.scan(
                TableName=self.table_name,
                FilterExpression="moderation_result = :result",
                ExpressionAttributeValues={
                    ":result": {"S": "rejected"}
                },
                Select="COUNT"
            )
            return response.get("Count", 0)
        except Exception as e:
            print(f"拒否モデレーション数の取得中にエラーが発生しました: {str(e)}")
            raise
