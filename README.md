# カープコネクト モデレーションシステム

AWS Bedrockを活用した国産LLM（大規模言語モデル）を使用して、カープファンコミュニティサイト「カープコネクト」の掲示板投稿内容をリアルタイムで分析し、不適切な表現を自動検知する機能を実装したシステムです。

## 🚀 機能概要

- **AI搭載コンテンツモデレーション**: AWS Bedrock経由でLLMを使用した自動内容チェック
- **リアルタイム分析**: 投稿・コメント・プロフィールの即座な適切性判定
- **多言語対応**: 日本語コンテンツに特化したモデレーション
- **統計情報**: モデレーション履歴と承認率の可視化
- **スケーラブル**: AWS Lambda + API Gateway + DynamoDBによるサーバーレス構成

## 🏗️ アーキテクチャ

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   フロントエンド   │    │    API Gateway   │    │   Lambda関数    │
│   (Next.js)     │◄──►│                │◄──►│  (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   DynamoDB      │
                                              │   (データ保存)    │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │  AWS Bedrock    │
                                              │   (LLM API)     │
                                              └─────────────────┘
```

## 🛠️ 技術スタック

### バックエンド
- **FastAPI**: Pythonベースの高速Webフレームワーク
- **AWS Lambda**: サーバーレス実行環境
- **Mangum**: FastAPI ↔ Lambda アダプター
- **boto3**: AWS SDK for Python

### フロントエンド
- **Next.js**: Reactベースのフレームワーク
- **Tailwind CSS**: ユーティリティファーストCSS
- **Axios**: HTTPクライアント

### インフラストラクチャ
- **Terraform**: インフラのコード化
- **AWS DynamoDB**: NoSQLデータベース
- **AWS API Gateway**: RESTful API管理
- **AWS IAM**: アクセス制御

### AI/ML
- **AWS Bedrock**: マネージドLLMサービス
- **Claude v2**: Anthropicの大規模言語モデル

## 📋 前提条件

- AWS CLI がインストール済み
- Terraform がインストール済み
- Python 3.9以上
- Node.js 16以上
- AWSアカウント（Bedrockアクセス権限付き）

## 🚀 セットアップ手順

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd carp-connect-moderation
```

### 2. AWS認証情報の設定
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="ap-northeast-1"
```

### 3. 環境変数ファイルの作成
```bash
cd backend
cp env.example .env
# .envファイルを編集して適切な値を設定
```

### 4. 依存関係のインストール
```bash
# バックエンド
cd backend
pip install -r requirements.txt

# フロントエンド
cd ../frontend
npm install
```

### 5. インフラストラクチャのデプロイ
```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

### 6. アプリケーションの起動
```bash
# バックエンド（開発モード）
cd backend
python -m uvicorn app.main:app --reload

# フロントエンド（別ターミナル）
cd frontend
npm run dev
```

## 🔧 設定項目

### 環境変数
- `AWS_REGION`: AWSリージョン（デフォルト: ap-northeast-1）
- `AWS_ACCESS_KEY_ID`: AWSアクセスキーID
- `AWS_SECRET_ACCESS_KEY`: AWSシークレットアクセスキー
- `BEDROCK_MODEL_ID`: 使用するBedrockモデルID（デフォルト: anthropic.claude-v2）
- `DYNAMODB_*_TABLE`: 各DynamoDBテーブル名
- `JWT_SECRET_KEY`: JWT署名用シークレットキー

### Bedrockモデル設定
現在は `anthropic.claude-v2` を使用していますが、以下のモデルにも対応可能です：
- `anthropic.claude-3-sonnet-20240229-v1:0`
- `anthropic.claude-3-haiku-20240307-v1:0`
- `amazon.titan-text-express-v1`

## 📊 使用方法

### 1. モデレーションチェック
フロントエンドのフォームにコンテンツを入力し、「モデレーションチェック」ボタンをクリックします。

### 2. 結果の確認
- **承認**: コンテンツが適切と判断された場合
- **拒否**: 不適切な内容と判断された場合
- **スコア**: 0.0〜1.0の適切性スコア
- **理由**: 判断理由の説明

### 3. 履歴の確認
`/api/moderation/history` エンドポイントでモデレーション履歴を取得できます。

## 🔍 API エンドポイント

### モデレーション
- `POST /api/moderation/check`: コンテンツのモデレーションチェック
- `GET /api/moderation/history`: モデレーション履歴の取得
- `GET /api/moderation/stats`: 統計情報の取得

### 認証
- `POST /api/auth/login`: ユーザーログイン
- `POST /api/auth/register`: ユーザー登録

## 🧪 テスト

### バックエンドテスト
```bash
cd backend
python -m pytest tests/
```

### フロントエンドテスト
```bash
cd frontend
npm test
```

## 📈 監視とログ

- **CloudWatch Logs**: Lambda関数の実行ログ
- **CloudWatch Metrics**: API Gatewayのメトリクス
- **DynamoDB Streams**: データベース変更の追跡

## 🔒 セキュリティ

- **IAMロール**: 最小権限の原則に基づくアクセス制御
- **VPC**: 必要に応じてプライベートサブネットでの実行
- **暗号化**: 転送時・保存時のデータ暗号化
- **監査ログ**: すべてのアクセスの記録

## 🚨 トラブルシューティング

### よくある問題

1. **Bedrockアクセス権限エラー**
   - IAMロールにBedrock権限が付与されているか確認
   - リージョンが正しく設定されているか確認

2. **DynamoDB接続エラー**
   - テーブルが正しく作成されているか確認
   - IAMロールにDynamoDB権限が付与されているか確認

3. **Lambda関数のタイムアウト**
   - 関数のタイムアウト設定を確認
   - Bedrock APIの応答時間を確認

## 📝 開発者向け情報

### コード構造
```
├── backend/                 # バックエンドコード
│   ├── app/
│   │   ├── routes/         # APIルート
│   │   ├── services/       # ビジネスロジック
│   │   ├── db/            # データベース層
│   │   └── config.py      # 設定
│   └── requirements.txt    # Python依存関係
├── frontend/               # フロントエンドコード
│   ├── src/
│   │   ├── components/    # Reactコンポーネント
│   │   ├── services/      # API呼び出し
│   │   └── pages/         # ページコンポーネント
│   └── package.json       # Node.js依存関係
└── infra/                  # インフラストラクチャ
    ├── terraform/         # Terraformコード
    └── scripts/           # デプロイスクリプト
```

### 拡張ポイント
- **新しいモデレーションルール**: `ModerationService`クラスの拡張
- **追加のAIモデル**: Bedrockの他のモデルへの対応
- **カスタムメトリクス**: CloudWatchカスタムメトリクスの追加

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

問題や質問がある場合は、GitHubのIssuesページで報告してください。

---

**カープコネクト** - 広島カープファンのための安全なコミュニティサイト 🏟️⚾

## 🎯 現在の進捗状況（2025年8月20日）

### ✅ 完了済み
- [x] **インフラストラクチャのデプロイ完了！**
- [x] **AWSリソース作成完了**
  - DynamoDBテーブル（5個）
  - IAMロールとポリシー
  - Lambda関数
  - API Gateway
  - Bedrockアクセスポリシー
- [x] **Terraform設定完了**
- [x] **バックエンド・フロントエンドコード実装完了**

### 🚀 次のステップ
1. **アプリケーションの起動**
   - バックエンド: `python -m uvicorn app.main:app --reload`
   - フロントエンド: `npm run dev`
2. **動作確認**
   - フロントエンド: http://localhost:3000
   - バックエンド: http://localhost:8000
3. **モデレーション機能のテスト**

### 🔑 重要な情報
- **AWSリージョン**: ap-northeast-1（東京）
- **プロジェクト名**: carp-connect-moderation
- **Terraform状態**: 完了済み
- **環境変数**: `.env`ファイルで設定が必要

### 📁 主要ディレクトリ
- **プロジェクトルート**: `C:\Users\yamas\Downloads\carp-connect-moderation\`
- **Terraform設定**: `infra/terraform\`
- **バックエンド**: `backend\`
- **フロントエンド**: `frontend\`
