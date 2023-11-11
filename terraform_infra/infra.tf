provider "aws" {
  region = "us-west-2"
}

resource "aws_dynamodb_table" "example" {
  name         = "DTABLE_NAME_TO_BE_CHANGED"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "DB_ID"

  attribute {
    name = "DB_ID"
    type = "S"
  }
}

resource "aws_dynamodb_table" "Records_Deleted" {
  name         = "Records_Deleted"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "DB_ID"

  attribute {
    name = "DB_ID"
    type = "S"
  }
}


resource "aws_iam_role" "lambda_iam_role" {
  name = "lambda_iam_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
      },
    ],
  })
}

resource "aws_iam_role_policy" "lambda_iam_policy" {
  name = "lambda_iam_policy"
  role = aws_iam_role.lambda_iam_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "dynamodb:CreateBackup",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ],
        Effect   = "Allow",
        Resource = "*"
      },
    ],
  })
}

resource "aws_lambda_function" "lambda_function" {
  filename         = "item_purge.py.zip"
  function_name    = "item_purge_lambda"
  role             = aws_iam_role.lambda_iam_role.arn
  handler          = "item_purge.lambda_handler"
  source_code_hash = filebase64sha256("item_purge.py.zip")
  runtime          = "python3.8"

  depends_on = [aws_iam_role_policy.lambda_iam_policy]
}
