# IAMロールとポリシーの設定
resource "aws_iam_role" "lambda_role" {
  name = "carp-connect-moderation-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Bedrock用のポリシー
resource "aws_iam_policy" "bedrock_policy" {
  name        = "carp-connect-moderation-bedrock-policy"
  description = "Bedrock用のポリシー"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:ListFoundationModels",
          "bedrock:GetFoundationModel",
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:ListProvisionedModelThroughputs",
          "bedrock:GetProvisionedModelThroughput"
        ]
        Resource = [
          "arn:aws:bedrock:ap-northeast-1::foundation-model/*",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/amazon.titan-text-express-v1",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/amazon.titan-text-lite-v1", 
          "arn:aws:bedrock:ap-northeast-1::foundation-model/amazon.titan-embed-text-v1",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/amazon.titan-embed-text-v2",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/amazon.nova-*",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/anthropic.claude-*",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/ai21.j2-*",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/cohere.command-*",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/cohere.embed-*",
          "arn:aws:bedrock:ap-northeast-1::foundation-model/cohere.rerank-*"
        ]
      }
    ]
  })
}

# DynamoDB用のポリシー
resource "aws_iam_policy" "dynamodb_policy" {
  name        = "carp-connect-moderation-dynamodb-policy"
  description = "DynamoDB用のポリシー"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchGetItem",
          "dynamodb:BatchWriteItem"
        ]
        Resource = [
          "arn:aws:dynamodb:ap-northeast-1:${data.aws_caller_identity.current.account_id}:table/carp-connect-moderation-*"
        ]
      }
    ]
  })
}

# ローカル開発用の包括的ポリシー
resource "aws_iam_policy" "local_development_policy" {
  name        = "carp-connect-moderation-local-development-policy"
  description = "ローカル開発用の包括的なポリシー"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:*"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:*"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:GetUser",
          "iam:GetUserPolicy",
          "iam:ListAttachedUserPolicies",
          "iam:ListUserPolicies"
        ]
        Resource = "*"
      }
    ]
  })
}

# ポリシーをロールにアタッチ
resource "aws_iam_role_policy_attachment" "lambda_bedrock" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.bedrock_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

# 現在のAWSアカウントIDを取得
data "aws_caller_identity" "current" {} 