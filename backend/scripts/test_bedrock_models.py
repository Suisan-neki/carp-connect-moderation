#!/usr/bin/env python3
"""
Bedrockモデルの自動テストスクリプト
利用可能なモデルIDを自動で見つけて、最適な設定を提案します
"""

import boto3
import json
import sys
import os
from typing import List, Dict, Any

# 設定ファイルのパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
from config import settings

def test_bedrock_access():
    """Bedrockへのアクセス権限をテスト"""
    try:
        bedrock = boto3.client(
            'bedrock-runtime',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        return True, bedrock
    except Exception as e:
        return False, str(e)

def list_available_models(bedrock_client) -> List[Dict[str, Any]]:
    """利用可能なモデルを一覧取得"""
    try:
        response = bedrock_client.list_foundation_models()
        return response.get('modelSummaries', [])
    except Exception as e:
        print(f"モデル一覧の取得に失敗: {e}")
        return []

def test_model_invocation(bedrock_client, model_id: str) -> bool:
    """特定のモデルでテスト呼び出しを実行"""
    try:
        # 軽量なテストプロンプト
        test_prompt = "Hello, please respond with 'OK' only."
        
        if model_id.startswith('anthropic.'):
            # Anthropicモデル用
            body = json.dumps({
                "prompt": test_prompt,
                "max_tokens_to_sample": 10,
                "temperature": 0.1
            })
        elif model_id.startswith('amazon.'):
            # Amazon Titan用
            body = json.dumps({
                "inputText": test_prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 10,
                    "temperature": 0.1
                }
            })
        else:
            # その他のモデル用
            body = json.dumps({
                "prompt": test_prompt,
                "max_tokens": 10,
                "temperature": 0.1
            })
        
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body
        )
        
        print(f"[SUCCESS] {model_id}: 成功")
        return True
        
    except Exception as e:
        print(f"[ERROR] {model_id}: 失敗 - {str(e)}")
        return False

def find_working_models(bedrock_client) -> List[str]:
    """動作するモデルIDを見つける"""
    print("[INFO] 利用可能なモデルを確認中...")
    
    # テスト対象のモデルID（優先順位順）
    test_models = [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "amazon.titan-text-express-v1",
        "anthropic.claude-v2",
        "anthropic.claude-instant-v1"
    ]
    
    working_models = []
    
    for model_id in test_models:
        print(f"\n[TEST] {model_id} をテスト中...")
        if test_model_invocation(bedrock_client, model_id):
            working_models.append(model_id)
    
    return working_models

def update_env_file(working_model: str):
    """動作するモデルIDで.envファイルを更新"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    
    try:
        # .envファイルを読み込み
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # BEDROCK_MODEL_IDを更新
        import re
        pattern = r'BEDROCK_MODEL_ID=.*'
        replacement = f'BEDROCK_MODEL_ID={working_model}'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
        else:
            content += f'\nBEDROCK_MODEL_ID={working_model}'
        
        # ファイルに書き込み
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n[SUCCESS] .envファイルを更新しました: BEDROCK_MODEL_ID={working_model}")
        
    except Exception as e:
        print(f"[ERROR] .envファイルの更新に失敗: {e}")

def main():
    """メイン処理"""
    print("[START] Bedrockモデルの自動テストを開始します...")
    print(f"[INFO] リージョン: {settings.AWS_REGION}")
    print(f"[INFO] AWSキー: {'設定済み' if settings.AWS_ACCESS_KEY_ID else '未設定'}")
    
    # Bedrockアクセステスト
    access_ok, bedrock_client = test_bedrock_access()
    if not access_ok:
        print(f"[ERROR] Bedrockアクセスに失敗: {bedrock_client}")
        print("IAM権限を確認してください")
        return
    
    print("[SUCCESS] Bedrockアクセス成功")
    
    # 動作するモデルを探す
    working_models = find_working_models(bedrock_client)
    
    if not working_models:
        print("\n[ERROR] 動作するモデルが見つかりませんでした")
        print("以下を確認してください:")
        print("1. IAM権限が正しく設定されているか")
        print("2. リージョンで利用可能なモデルか")
        print("3. モデルIDが正しいか")
        return
    
    print(f"\n[SUCCESS] 動作するモデルが見つかりました: {working_models[0]}")
    
    # 最適なモデルで.envファイルを更新
    update_env_file(working_models[0])
    
    print("\n[NEXT] 次の手順:")
    print("1. サーバーを再起動してください")
    print("2. APIを再テストしてください")
    print(f"3. 使用モデル: {working_models[0]}")

if __name__ == "__main__":
    main() 