import uuid
import time
import json
import boto3
import logging
from typing import List, Dict, Any
from ..db.repositories.moderation_repository import ModerationRepository
from ..config import settings

logger = logging.getLogger(__name__)

class ModerationService:
    def __init__(self):
        self.moderation_repository = ModerationRepository()
        # 開発/ローカル用のモックモード判定（AWS認証情報が無い、またはDEBUGが有効）
        self.mock_mode = (
            settings.DEBUG
            or not settings.AWS_ACCESS_KEY_ID
            or not settings.AWS_SECRET_ACCESS_KEY
        )
        if not self.mock_mode:
            self.bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        else:
            self.bedrock_client = None
        self.model_id = settings.BEDROCK_MODEL_ID

    async def check_content(self, content: str, content_type: str) -> Dict[str, Any]:
        """
        コンテンツをLLMでモデレーションチェックします。
        """
        try:
            # LLMにプロンプトを送信
            prompt = self._create_moderation_prompt(content)
            response = self._invoke_llm(prompt, content)
            
            # レスポンスを解析
            moderation_result = self._parse_llm_response(response)
            
            # モデレーション結果をデータベースに保存
            moderation_id = str(uuid.uuid4())
            await self.moderation_repository.create_moderation_record({
                "moderation_id": moderation_id,
                "content_id": "temp-" + moderation_id,  # 一時的なID
                "content_type": content_type,
                "original_content": content,
                "moderation_result": moderation_result["result"],
                "moderation_reason": moderation_result["reason"],
                "moderation_score": moderation_result["score"],
                "created_at": int(time.time())
            })
            
            return {
                "moderation_id": moderation_id,
                "content": content,
                "result": moderation_result["result"],
                "reason": moderation_result["reason"],
                "score": moderation_result["score"],
                "created_at": int(time.time())
            }
        except Exception as e:
            logger.error(f"モデレーションチェック中にエラーが発生しました: {str(e)}")
            raise

    async def get_moderation_history(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        モデレーション履歴を取得します。
        """
        try:
            return await self.moderation_repository.get_moderation_history(limit, offset)
        except Exception as e:
            logger.error(f"モデレーション履歴の取得中にエラーが発生しました: {str(e)}")
            raise

    async def get_moderation_stats(self) -> Dict[str, Any]:
        """
        モデレーション統計情報を取得します。
        """
        try:
            total_count = await self.moderation_repository.get_total_moderation_count()
            approved_count = await self.moderation_repository.get_approved_moderation_count()
            rejected_count = await self.moderation_repository.get_rejected_moderation_count()
            
            return {
                "total_count": total_count,
                "approved_count": approved_count,
                "rejected_count": rejected_count,
                "approval_rate": approved_count / total_count if total_count > 0 else 0
            }
        except Exception as e:
            logger.error(f"モデレーション統計情報の取得中にエラーが発生しました: {str(e)}")
            raise

    def _create_moderation_prompt(self, content: str) -> str:
        """
        モデレーション用のプロンプトを作成します。
        """
        return f"""
        あなたはカープファンのコミュニティサイト「カープコネクト」のコンテンツモデレーターです。
        以下のコンテンツが適切かどうかを判断してください。

        不適切なコンテンツの例：
        - 暴力的な表現
        - 差別的な表現
        - 性的な表現
        - 誹謗中傷
        - スパム
        - 個人情報の漏洩

        コンテンツ：
        """
        {content}
        """

        以下の形式でJSON形式で回答してください：
        {{
          "result": "approved" または "rejected",
          "reason": "判断理由を簡潔に説明",
          "score": 0.0から1.0の数値（1.0が最も適切）
        }}
        """

    def _invoke_llm(self, prompt: str, content: str) -> str:
        """
        AWS Bedrock経由でLLMを呼び出します。モックモードではローカルで擬似結果を返します。
        """
        try:
            if self.mock_mode:
                lowered = (content or "").lower()
                is_rejected = any(kw in lowered for kw in [
                    "violence", "hate", "discrimination", "spam", "harassment"
                ])
                mock = {
                    "result": "rejected" if is_rejected else "approved",
                    "reason": "開発モード（モック）で自動判定しました",
                    "score": 0.3 if is_rejected else 0.9,
                }
                return json.dumps(mock)

            body = json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.1,
                "top_p": 0.9,
            })
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body.get('completion', '')
        except Exception as e:
            logger.error(f"LLM呼び出し中にエラーが発生しました: {str(e)}")
            # フォールバック: デフォルト承認のJSONを返して処理を継続
            return json.dumps({
                "result": "approved",
                "reason": "LLM呼び出しに失敗したためデフォルトで承認しました。",
                "score": 0.5
            })

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        LLMのレスポンスを解析します。
        """
        try:
            # JSON部分を抽出
            json_str = response.strip()
            if not json_str.startswith('{'):
                # JSONが見つからない場合、テキスト内からJSONを探す
                import re
                json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    # JSONが見つからない場合はデフォルト値を返す
                    return {
                        "result": "approved",
                        "reason": "モデレーション結果の解析に失敗しました。デフォルトで承認します。",
                        "score": 0.5
                    }
            
            result = json.loads(json_str)
            return {
                "result": result.get("result", "approved"),
                "reason": result.get("reason", "理由が提供されていません"),
                "score": float(result.get("score", 0.5))
            }
        except Exception as e:
            logger.error(f"LLMレスポンスの解析中にエラーが発生しました: {str(e)}")
            # エラーが発生した場合はデフォルト値を返す
            return {
                "result": "approved",
                "reason": f"モデレーション結果の解析に失敗しました: {str(e)}",
                "score": 0.5
            }
