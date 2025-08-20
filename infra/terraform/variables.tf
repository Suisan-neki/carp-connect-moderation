variable "aws_region" {
  description = "AWSリージョン"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "プロジェクト名"
  type        = string
  default     = "carp-connect-moderation"
}

variable "bedrock_model_id" {
  description = "使用するBedrockモデルID"
  type        = string
  default     = "anthropic.claude-v2"
}

variable "environment" {
  description = "環境（dev, staging, prod）"
  type        = string
  default     = "dev"
}

variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
  default = {
    Project     = "carp-connect-moderation"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
} 