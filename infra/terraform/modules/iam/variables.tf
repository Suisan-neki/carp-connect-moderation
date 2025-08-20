variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "dynamodb_table_arns" {
  description = "DynamoDBテーブルのARNリスト"
  type        = list(string)
}

variable "bedrock_model_id" {
  description = "使用するBedrockモデルID"
  type        = string
}

variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
} 