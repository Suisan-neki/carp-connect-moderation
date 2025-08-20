resource "aws_dynamodb_table" "user_table" {
  name           = var.user_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  
  attribute {
    name = "user_id"
    type = "S"
  }
  
  tags = var.tags
}

resource "aws_dynamodb_table" "board_table" {
  name           = var.board_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "board_id"
  
  attribute {
    name = "board_id"
    type = "S"
  }
  
  tags = var.tags
}

resource "aws_dynamodb_table" "post_table" {
  name           = var.post_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "post_id"
  
  attribute {
    name = "post_id"
    type = "S"
  }
  
  tags = var.tags
}

resource "aws_dynamodb_table" "comment_table" {
  name           = var.comment_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "comment_id"
  
  attribute {
    name = "comment_id"
    type = "S"
  }
  
  tags = var.tags
}

resource "aws_dynamodb_table" "moderation_table" {
  name           = var.moderation_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "moderation_id"
  
  attribute {
    name = "moderation_id"
    type = "S"
  }
  
  tags = var.tags
} 