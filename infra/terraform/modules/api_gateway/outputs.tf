output "api_gateway_id" {
  description = "API GatewayのID"
  value       = aws_api_gateway_rest_api.main.id
}

output "api_gateway_url" {
  description = "API GatewayのエンドポイントURL"
  value       = "${aws_api_gateway_rest_api.main.execution_arn}/prod"
}

output "api_gateway_execution_arn" {
  description = "API Gatewayの実行ARN"
  value       = aws_api_gateway_rest_api.main.execution_arn
} 
 