variable "user_table_name" {
  description = "ユーザーテーブル名"
  type        = string
}

variable "board_table_name" {
  description = "掲示板テーブル名"
  type        = string
}

variable "post_table_name" {
  description = "投稿テーブル名"
  type        = string
}

variable "comment_table_name" {
  description = "コメントテーブル名"
  type        = string
}

variable "moderation_table_name" {
  description = "モデレーションテーブル名"
  type        = string
}

variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
} 