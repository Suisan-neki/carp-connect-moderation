data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../../backend"
  output_path = "${path.module}/lambda.zip"
  excludes    = ["__pycache__", "*.pyc", ".env", "env.example"]
}

resource "aws_lambda_function" "main" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.project_name}-function"
  role            = var.lambda_role_arn
  handler         = "app.main.handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 512

  environment {
    variables = var.environment_variables
  }

  tags = var.tags
}

resource "aws_lambda_function_url" "main" {
  function_name      = aws_lambda_function.main.function_name
  authorization_type = "NONE"
} 