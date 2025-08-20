output "lambda_role_arn" {
  description = "Lambda実行ロールのARN"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_role_name" {
  description = "Lambda実行ロールの名前"
  value       = aws_iam_role.lambda_role.name
}

output "dynamodb_policy_arn" {
  description = "DynamoDBアクセスポリシーのARN"
  value       = aws_iam_policy.dynamodb_policy.arn
}

output "bedrock_policy_arn" {
  description = "BedrockアクセスポリシーのARN"
  value       = aws_iam_policy.bedrock_policy.arn
} 