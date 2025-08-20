variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "model_id" {
  description = "使用するBedrockモデルID"
  type        = string
}

variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
} 