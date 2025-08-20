import os
from pydantic import BaseSettings

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
    
    # CORS設定
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # JWT設定
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24  # 24時間
    
    class Config:
        env_file = ".env"

settings = Settings()
