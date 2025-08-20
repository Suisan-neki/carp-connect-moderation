output "bedrock_policy_arn" {
  description = "BedrockアクセスポリシーのARN"
  value       = aws_iam_policy.bedrock_policy.arn
}

output "bedrock_policy_name" {
  description = "Bedrockアクセスポリシーの名前"
  value       = aws_iam_policy.bedrock_policy.name
} 