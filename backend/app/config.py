import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union

class Settings(BaseSettings):
	# アプリケーション設定
	APP_NAME: str = "Carp Connect Moderation API"
	APP_VERSION: str = "0.1.0"
	DEBUG: bool = os.getenv("DEBUG", "False") == "True"
	
	# AWS設定
	AWS_REGION: str = os.getenv("AWS_REGION", "ap-northeast-1")
	AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
	AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
	
	# DynamoDB設定
	DYNAMODB_USER_TABLE: str = os.getenv("DYNAMODB_USER_TABLE", "carp-connect-moderation-users")
	DYNAMODB_BOARD_TABLE: str = os.getenv("DYNAMODB_BOARD_TABLE", "carp-connect-moderation-boards")
	DYNAMODB_POST_TABLE: str = os.getenv("DYNAMODB_POST_TABLE", "carp-connect-moderation-posts")
	DYNAMODB_COMMENT_TABLE: str = os.getenv("DYNAMODB_COMMENT_TABLE", "carp-connect-moderation-comments")
	DYNAMODB_MODERATION_TABLE: str = os.getenv("DYNAMODB_MODERATION_TABLE", "carp-connect-moderation-moderation")
	
	# Bedrock設定
	BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2")
	
	# CORS設定（カンマ区切りの文字列 or JSON配列の両方対応）
	CORS_ORIGINS: List[str] = ["*"]
	
	# JWT設定
	JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
	JWT_ALGORITHM: str = "HS256"
	JWT_EXPIRATION_MINUTES: int = 60 * 24  # 24時間
	
	# Pydantic v2 settings config
	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

	@field_validator("CORS_ORIGINS", mode="before")
	@classmethod
	def parse_cors_origins(cls, v: Union[str, List[str]]):
		# 文字列ならカンマで分割、配列ならそのまま
		if isinstance(v, str):
			v = v.strip()
			if not v:
				return ["*"]
			# JSON配列形式の可能性も考慮
			if v.startswith("[") and v.endswith("]"):
				try:
					import json as _json
					arr = _json.loads(v)
					return [str(x).strip() for x in arr]
				except Exception:
					return [s.strip() for s in v.split(",") if s.strip()]
			return [s.strip() for s in v.split(",") if s.strip()]
		if isinstance(v, list):
			return [str(s).strip() for s in v]
		return ["*"]

settings = Settings()
