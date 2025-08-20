terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# DynamoDBテーブル
module "dynamodb" {
  source = "./modules/dynamodb"
  
  user_table_name       = "${var.project_name}-users"
  board_table_name      = "${var.project_name}-boards"
  post_table_name       = "${var.project_name}-posts"
  comment_table_name    = "${var.project_name}-comments"
  moderation_table_name = "${var.project_name}-moderation"
  
  tags = var.tags
}

# IAMロール
module "iam" {
  source = "./modules/iam"
  
  project_name = var.project_name
  
  dynamodb_table_arns = [
    module.dynamodb.user_table_arn,
    module.dynamodb.board_table_arn,
    module.dynamodb.post_table_arn,
    module.dynamodb.comment_table_arn,
    module.dynamodb.moderation_table_arn
  ]
  
  bedrock_model_id = var.bedrock_model_id
  
  tags = var.tags
}

# Lambda関数
module "lambda" {
  source = "./modules/lambda"
  
  project_name    = var.project_name
  lambda_role_arn = module.iam.lambda_role_arn
  
  environment_variables = {
    DYNAMODB_USER_TABLE       = module.dynamodb.user_table_name
    DYNAMODB_BOARD_TABLE      = module.dynamodb.board_table_name
    DYNAMODB_POST_TABLE       = module.dynamodb.post_table_name
    DYNAMODB_COMMENT_TABLE    = module.dynamodb.comment_table_name
    DYNAMODB_MODERATION_TABLE = module.dynamodb.moderation_table_name
    BEDROCK_MODEL_ID          = var.bedrock_model_id
  }
  
  tags = var.tags
}

# API Gateway
module "api_gateway" {
  source = "./modules/api_gateway"
  
  project_name        = var.project_name
  lambda_invoke_arn   = module.lambda.lambda_invoke_arn
  lambda_function_name = module.lambda.lambda_function_name
  
  tags = var.tags
}
