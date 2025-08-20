variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "lambda_invoke_arn" {
  description = "Lambda関数の呼び出しARN"
  type        = string
}

variable "lambda_function_name" {
  description = "Lambda関数の名前"
  type        = string
}

variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
} 