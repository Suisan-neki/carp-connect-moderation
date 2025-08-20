output "lambda_function_arn" {
  description = "Lambda関数のARN"
  value       = aws_lambda_function.main.arn
}

output "lambda_function_name" {
  description = "Lambda関数の名前"
  value       = aws_lambda_function.main.function_name
}

output "lambda_invoke_arn" {
  description = "Lambda関数の呼び出しARN"
  value       = aws_lambda_function.main.invoke_arn
}

output "lambda_function_url" {
  description = "Lambda関数のURL"
  value       = aws_lambda_function_url.main.function_url
} 