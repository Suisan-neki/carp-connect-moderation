output "api_gateway_url" {
  description = "API GatewayのエンドポイントURL"
  value       = module.api_gateway.api_gateway_url
}

output "dynamodb_table_names" {
  description = "作成されたDynamoDBテーブル名"
  value = {
    user_table       = module.dynamodb.user_table_name
    board_table      = module.dynamodb.board_table_name
    post_table       = module.dynamodb.post_table_name
    comment_table    = module.dynamodb.comment_table_name
    moderation_table = module.dynamodb.moderation_table_name
  }
}

output "lambda_function_arn" {
  description = "Lambda関数のARN"
  value       = module.lambda.lambda_function_arn
}

output "bedrock_policy_arn" {
  description = "BedrockアクセスポリシーのARN"
  value       = module.iam.bedrock_policy_arn
} 