from typing import Any, Dict, List, Optional
from ...config import settings

try:
    import boto3  # type: ignore
except Exception:  # pragma: no cover
    boto3 = None  # type: ignore


_in_memory_store: List[Dict[str, Any]] = []


class FakeDynamoDBClient:
    def put_item(self, TableName: str, Item: Dict[str, Any]) -> None:
        _in_memory_store.append(Item)

    def scan(
        self,
        TableName: str,
        Limit: Optional[int] = None,
        Select: Optional[str] = None,
        FilterExpression: Optional[str] = None,
        ExpressionAttributeValues: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        items = list(_in_memory_store)

        # COUNT mode
        if Select == "COUNT":
            if FilterExpression and ExpressionAttributeValues:
                expected = ExpressionAttributeValues.get(":result", {}).get("S")
                count = sum(1 for it in items if it.get("moderation_result", {}).get("S") == expected)
                return {"Count": count}
            return {"Count": len(items)}

        # Filter by moderation_result if requested
        if FilterExpression and ExpressionAttributeValues:
            expected = ExpressionAttributeValues.get(":result", {}).get("S")
            items = [it for it in items if it.get("moderation_result", {}).get("S") == expected]

        if Limit is not None:
            items = items[:Limit]

        return {"Items": items}


def _should_use_fake() -> bool:
    # Use fake when boto3 is unavailable or creds are missing
    if boto3 is None:
        return True
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        return True
    return False


def get_dynamodb_client():
    if _should_use_fake():
        return FakeDynamoDBClient()
    return boto3.client(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )