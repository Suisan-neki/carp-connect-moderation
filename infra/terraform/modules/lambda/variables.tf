variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "lambda_role_arn" {
  description = "Lambda実行ロールのARN"
  type        = string
}

variable "environment_variables" {
  description = "Lambda関数の環境変数"
  type        = map(string)
}

variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
} 