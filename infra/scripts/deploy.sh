#!/bin/bash

# 環境変数の設定
export AWS_REGION="ap-northeast-1"
export PROJECT_NAME="carp-connect-moderation"

# フロントエンドのビルドとデプロイ
echo "Building and deploying frontend..."
cd ../../frontend
npm install
npm run build
aws s3 sync out/ s3://$PROJECT_NAME-frontend --delete
aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_DISTRIBUTION_ID --paths "/*"

# バックエンドのビルドとデプロイ
echo "Building and deploying backend..."
cd ../backend
pip install -r requirements.txt
zip -r lambda.zip app/ requirements.txt
aws lambda update-function-code --function-name $PROJECT_NAME-api --zip-file fileb://lambda.zip

# Terraformのデプロイ
echo "Deploying infrastructure with Terraform..."
cd ../infra/terraform
terraform init
terraform apply -auto-approve

echo "Deployment completed successfully!"
