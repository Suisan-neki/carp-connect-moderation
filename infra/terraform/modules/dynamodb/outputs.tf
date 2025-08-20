output "user_table_name" {
  description = "ユーザーテーブル名"
  value       = aws_dynamodb_table.user_table.name
}

output "board_table_name" {
  description = "掲示板テーブル名"
  value       = aws_dynamodb_table.board_table.name
}

output "post_table_name" {
  description = "投稿テーブル名"
  value       = aws_dynamodb_table.post_table.name
}

output "comment_table_name" {
  description = "コメントテーブル名"
  value       = aws_dynamodb_table.comment_table.name
}

output "moderation_table_name" {
  description = "モデレーションテーブル名"
  value       = aws_dynamodb_table.moderation_table.name
}

output "user_table_arn" {
  description = "ユーザーテーブルのARN"
  value       = aws_dynamodb_table.user_table.arn
}

output "board_table_arn" {
  description = "掲示板テーブルのARN"
  value       = aws_dynamodb_table.board_table.arn
}

output "post_table_arn" {
  description = "投稿テーブルのARN"
  value       = aws_dynamodb_table.post_table.arn
}

output "comment_table_arn" {
  description = "コメントテーブルのARN"
  value       = aws_dynamodb_table.comment_table.arn
}

output "moderation_table_arn" {
  description = "モデレーションテーブルのARN"
  value       = aws_dynamodb_table.moderation_table.arn
} 