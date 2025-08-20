resource "aws_iam_policy" "bedrock_policy" {
  name        = "${var.project_name}-bedrock-policy"
  description = "Policy for accessing Amazon Bedrock"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "bedrock:InvokeModel",
          "bedrock:GetFoundationModel"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:bedrock:*:*:foundation-model/${var.model_id}"
      }
    ]
  })
  
  tags = var.tags
}
