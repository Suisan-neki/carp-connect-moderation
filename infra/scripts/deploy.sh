#!/bin/bash

# カープコネクトモデレーションシステムのデプロイスクリプト

set -e

echo "🚀 カープコネクトモデレーションシステムのデプロイを開始します..."

# 環境変数の確認
if [ -z "$AWS_REGION" ]; then
    echo "❌ AWS_REGIONが設定されていません"
    exit 1
fi

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ AWS認証情報が設定されていません"
    exit 1
fi

echo "📍 AWSリージョン: $AWS_REGION"

# Terraformの初期化
echo "🔧 Terraformの初期化中..."
cd infra/terraform
terraform init

# Terraformの実行計画確認
echo "📋 Terraformの実行計画を確認中..."
terraform plan

# ユーザー確認
read -p "デプロイを続行しますか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ デプロイをキャンセルしました"
    exit 1
fi

# Terraformの適用
echo "🚀 インフラストラクチャのデプロイ中..."
terraform apply -auto-approve

# 出力情報の表示
echo "✅ デプロイが完了しました！"
echo ""
echo "📊 デプロイ結果:"
terraform output

echo ""
echo "🎉 カープコネクトモデレーションシステムが正常にデプロイされました！"
echo ""
echo "次のステップ:"
echo "1. フロントエンドの起動: cd frontend && npm run dev"
echo "2. バックエンドの起動: cd backend && python -m uvicorn app.main:app --reload"
echo "3. ブラウザで http://localhost:3000 にアクセス"
