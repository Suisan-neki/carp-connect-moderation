#!/usr/bin/env python3
"""
特定のBedrockモデルをテストするスクリプト
異なるアプローチでモデルのアクセス可能性を確認
"""

import boto3
import os
import json
from botocore.exceptions import ClientError, NoCredentialsError

def test_model_access(model_id: str, bedrock_runtime):
    """特定のモデルへのアクセスをテスト"""
    print(f"[TEST] {model_id} をテスト中...")
    
    try:
        # モデルの詳細情報を取得
        bedrock = boto3.client('bedrock')
        model_info = bedrock.get_foundation_model(modelIdentifier=model_id)
        print(f"  [INFO] モデル情報: {model_info['modelDetails']['modelName']}")
        
        # 推論タイプを確認
        inference_types = model_info['modelDetails'].get('inferenceTypes', [])
        print(f"  [INFO] 推論タイプ: {inference_types}")
        
        # モデルIDの形式を確認
        print(f"  [INFO] モデルID: {model_info['modelDetails']['modelId']}")
        
        # 実際の呼び出しをテスト
        if "text" in str(inference_types).lower() or not inference_types:
            # テキスト生成モデルの場合
            if "anthropic" in model_id:
                request_body = {
                    "prompt": "\n\nHuman: Hello, this is a test.\n\nAssistant:",
                    "max_tokens": 10,
                    "temperature": 0.7
                }
            elif "amazon.titan" in model_id:
                request_body = {
                    "prompt": "Hello, this is a test.",
                    "maxTokens": 10,
                    "temperature": 0.7
                }
            elif "amazon.nova" in model_id:
                request_body = {
                    "prompt": "Hello, this is a test.",
                    "max_tokens": 10,
                    "temperature": 0.7
                }
            else:
                request_body = {
                    "prompt": "Hello, this is a test.",
                    "max_tokens": 10,
                    "temperature": 0.7
                }
            
            try:
                response = bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=json.dumps(request_body)
                )
                print(f"  [SUCCESS] {model_id}: アクセス可能")
                return True, "SUCCESS"
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                print(f"  [ERROR] {model_id}: {error_code} - {error_message}")
                return False, f"{error_code}: {error_message}"
                
        else:
            print(f"  [SKIP] {model_id}: テキスト生成モデルではありません")
            return False, "NOT_TEXT_MODEL"
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"  [ERROR] {model_id}: {error_code} - {error_message}")
        return False, f"{error_code}: {error_message}"
        
    except Exception as e:
        print(f"  [ERROR] {model_id}: 予期しないエラー - {e}")
        return False, str(e)

def main():
    """メイン処理"""
    print("[START] 特定のBedrockモデルのアクセステストを開始します...")
    
    try:
        # Bedrock Runtimeクライアントを作成
        bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'ap-northeast-1')
        )
        
        print(f"[INFO] リージョン: {os.getenv('AWS_REGION', 'ap-northeast-1')}")
        
        # テストするモデルのリスト（優先順位順）
        test_models = [
            "amazon.titan-text-express-v1",
            "amazon.titan-text-lite-v1", 
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "anthropic.claude-instant-v1",
            "amazon.nova-lite-v1:0",
            "amazon.nova-micro-v1:0"
        ]
        
        working_models = []
        
        for model_id in test_models:
            success, result = test_model_access(model_id, bedrock_runtime)
            if success:
                working_models.append((model_id, result))
                print(f"  [FOUND] 動作するモデル: {model_id}")
                break  # 最初の動作するモデルが見つかったら終了
        
        print(f"\n[RESULT] 動作するモデル数: {len(working_models)}")
        
        if working_models:
            print("[SUCCESS] 以下のモデルが利用可能です:")
            for model_id, result in working_models:
                print(f"  - {model_id}: {result}")
            
            # 推奨モデルを.envに設定
            recommended_model = working_models[0][0]
            print(f"\n[RECOMMENDATION] 推奨モデル: {recommended_model}")
            
            # .envファイルを更新
            env_file = ".env"
            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # BEDROCK_MODEL_IDを更新
                if "BEDROCK_MODEL_ID=" in content:
                    content = content.replace(
                        f"BEDROCK_MODEL_ID={os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-v2')}",
                        f"BEDROCK_MODEL_ID={recommended_model}"
                    )
                else:
                    content += f"\nBEDROCK_MODEL_ID={recommended_model}"
                
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"[SUCCESS] .envファイルを更新しました: BEDROCK_MODEL_ID={recommended_model}")
            else:
                print(f"[INFO] .envファイルが存在しません。手動でBEDROCK_MODEL_ID={recommended_model}を設定してください")
                
        else:
            print("[ERROR] 動作するモデルが見つかりませんでした")
            print("[INFO] 以下の可能性を確認してください:")
            print("  1. IAM権限が正しく設定されているか")
            print("  2. リージョンで利用可能なモデルか")
            print("  3. モデルIDが正しいか")
            print("  4. プロビジョニングされたスループットが必要か")
            
    except NoCredentialsError:
        print("[ERROR] AWS認証情報が見つかりません")
        print("[INFO] .envファイルにAWS_ACCESS_KEY_IDとAWS_SECRET_ACCESS_KEYを設定してください")
        
    except Exception as e:
        print(f"[ERROR] 予期しないエラー: {e}")

if __name__ == "__main__":
    main() 