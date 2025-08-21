#!/usr/bin/env python3
"""
利用可能なBedrockモデルを一覧表示するスクリプト
"""

import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError

def list_available_models():
    """利用可能なBedrockモデルを一覧表示"""
    print("[START] 利用可能なBedrockモデルを確認中...")
    
    try:
        # Bedrockクライアントを作成
        bedrock = boto3.client(
            'bedrock',
            region_name=os.getenv('AWS_REGION', 'ap-northeast-1')
        )
        
        # Bedrock Runtimeクライアントを作成（モデル呼び出し用）
        bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'ap-northeast-1')
        )
        
        print(f"[INFO] リージョン: {os.getenv('AWS_REGION', 'ap-northeast-1')}")
        
        # 利用可能なモデルを取得
        response = bedrock.list_foundation_models()
        
        print(f"[SUCCESS] 利用可能なモデル数: {len(response['modelSummaries'])}")
        print("\n[INFO] 利用可能なモデル一覧:")
        print("-" * 80)
        
        for model in response['modelSummaries']:
            model_id = model['modelId']
            provider = model['providerName']
            model_name = model['modelName']
            inference_type = model.get('inferenceTypes', [])
            
            print(f"モデルID: {model_id}")
            print(f"プロバイダー: {provider}")
            print(f"モデル名: {model_name}")
            print(f"推論タイプ: {', '.join(inference_type)}")
            print("-" * 80)
        
        # 特定のモデルをテスト
        print("\n[INFO] 主要モデルのアクセス権限をテスト中...")
        
        test_models = [
            "amazon.nova-pro-v1:0",
            "amazon.nova-lite-v1:0",
            "amazon.nova-micro-v1:0",
            "amazon.nova-canvas-v1:0",
            "amazon.nova-reel-v1:0",
            "amazon.nova-sonic-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0", 
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "amazon.titan-text-express-v1"
        ]
        
        working_models = []
        
        for model_id in test_models:
            try:
                print(f"[TEST] {model_id} をテスト中...")
                
                # 簡単なテスト用のプロンプト
                test_prompt = {
                    "prompt": "Hello, this is a test message.",
                    "maxTokens": 10,
                    "temperature": 0.7
                }
                
                # モデルによって異なるリクエスト形式
                if "anthropic" in model_id:
                    request_body = {
                        "prompt": f"\n\nHuman: {test_prompt['prompt']}\n\nAssistant:",
                        "max_tokens": test_prompt['maxTokens'],
                        "temperature": test_prompt['temperature']
                    }
                elif "amazon.titan" in model_id:
                    request_body = test_prompt
                elif "amazon.nova" in model_id:
                    request_body = {
                        "prompt": test_prompt['prompt'],
                        "max_tokens": test_prompt['maxTokens'],
                        "temperature": test_prompt['temperature']
                    }
                else:
                    request_body = test_prompt
                
                # モデルを呼び出し
                response = bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=json.dumps(request_body)
                )
                
                print(f"[SUCCESS] {model_id}: アクセス可能")
                working_models.append(model_id)
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                print(f"[ERROR] {model_id}: {error_code} - {error_message}")
                
            except Exception as e:
                print(f"[ERROR] {model_id}: 予期しないエラー - {e}")
        
        print(f"\n[RESULT] 動作するモデル数: {len(working_models)}")
        if working_models:
            print("[SUCCESS] 以下のモデルが利用可能です:")
            for model in working_models:
                print(f"  - {model}")
            
            # 最初の動作するモデルを.envに設定
            recommended_model = working_models[0]
            print(f"\n[RECOMMENDATION] 推奨モデル: {recommended_model}")
            print(f"[INFO] .envファイルのBEDROCK_MODEL_IDを{recommended_model}に更新してください")
        else:
            print("[ERROR] 動作するモデルが見つかりませんでした")
            print("[INFO] IAM権限の設定を確認してください")
            
    except NoCredentialsError:
        print("[ERROR] AWS認証情報が見つかりません")
        print("[INFO] .envファイルにAWS_ACCESS_KEY_IDとAWS_SECRET_ACCESS_KEYを設定してください")
        
    except Exception as e:
        print(f"[ERROR] 予期しないエラー: {e}")

if __name__ == "__main__":
    import json
    list_available_models() 