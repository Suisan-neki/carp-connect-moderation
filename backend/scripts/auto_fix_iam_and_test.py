#!/usr/bin/env python3
"""
自動IAM修正・テスト・再起動スクリプト
TerraformでIAM権限を更新し、ポリシーを再アタッチしてBedrockモデルをテストします
"""

import subprocess
import time
import sys
import os
import requests
import json
from typing import Optional, Tuple

def run_command(cmd: str, cwd: str = None) -> Tuple[bool, str]:
    """コマンドを実行して結果を返す"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            timeout=60
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output
    except subprocess.TimeoutExpired:
        return False, "コマンドがタイムアウトしました"
    except Exception as e:
        return False, str(e)

def update_terraform_infrastructure() -> bool:
    """Terraformでインフラを更新"""
    print("[INFO] Terraformでインフラを更新中...")
    
    terraform_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'infra', 'terraform')
    
    # terraform plan
    print("[INFO] terraform plan を実行中...")
    success, output = run_command("terraform plan", cwd=terraform_dir)
    if not success:
        print(f"[ERROR] terraform plan に失敗: {output}")
        return False
    
    print("[SUCCESS] terraform plan 完了")
    
    # terraform apply
    print("[INFO] terraform apply を実行中...")
    success, output = run_command("terraform apply -auto-approve", cwd=terraform_dir)
    if not success:
        print(f"[ERROR] terraform apply に失敗: {output}")
        return False
    
    print("[SUCCESS] terraform apply 完了")
    return True

def get_account_id() -> str:
    """AWSアカウントIDを取得"""
    try:
        result = subprocess.run(
            "aws sts get-caller-identity --query Account --output text",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "384504716192"  # デフォルト値
    except:
        return "384504716192"  # デフォルト値

def reattach_iam_policy() -> bool:
    """IAMポリシーを再アタッチ"""
    print("[INFO] IAMポリシーを再アタッチ中...")
    
    account_id = get_account_id()
    policy_arn = f"arn:aws:iam::{account_id}:policy/carp-connect-moderation-local-development-policy"
    
    # 既存のポリシーをデタッチ
    print("[INFO] 既存のポリシーをデタッチ中...")
    success, output = run_command(f"aws iam detach-user-policy --user-name suisan --policy-arn {policy_arn}")
    if not success:
        print(f"[WARN] ポリシーのデタッチに失敗（既に存在しない可能性）: {output}")
    
    # 新しいポリシーをアタッチ
    print("[INFO] 新しいポリシーをアタッチ中...")
    success, output = run_command(f"aws iam attach-user-policy --user-name suisan --policy-arn {policy_arn}")
    if not success:
        print(f"[ERROR] ポリシーのアタッチに失敗: {output}")
        return False
    
    print("[SUCCESS] IAMポリシーの再アタッチ完了")
    return True

def wait_for_iam_propagation():
    """IAM権限の反映を待つ"""
    print("[INFO] IAM権限の反映を待機中... (5分)")
    for i in range(30):  # 5分間
        print(f"[INFO] 待機中... {i+1}/30")
        time.sleep(10)

def test_bedrock_models() -> bool:
    """Bedrockモデルのテストを実行"""
    print("[INFO] Bedrockモデルの自動テストを実行中...")
    
    success, output = run_command(
        "python scripts/test_bedrock_models.py",
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    
    if success:
        print("[SUCCESS] Bedrockモデルのテストが完了しました")
        return True
    else:
        print(f"[ERROR] Bedrockモデルのテストに失敗: {output}")
        return False

def start_server(port: int) -> Optional[subprocess.Popen]:
    """サーバーを起動"""
    print(f"[INFO] サーバーをポート {port} で起動中...")
    
    try:
        # 環境変数を設定
        env = os.environ.copy()
        env['DEBUG'] = 'False'  # 実機モードで起動
        
        process = subprocess.Popen(
            f"python -m uvicorn app.main:app --host 127.0.0.1 --port {port}",
            shell=True,
            cwd=os.path.join(os.path.dirname(__file__), '..'),
            env=env
        )
        
        # 起動を待つ
        time.sleep(5)
        
        # プロセスが生きているか確認
        if process.poll() is None:
            print(f"[SUCCESS] サーバーがポート {port} で起動しました")
            return process
        else:
            print("[ERROR] サーバーの起動に失敗しました")
            return None
            
    except Exception as e:
        print(f"[ERROR] サーバー起動エラー: {e}")
        return None

def test_api(port: int) -> bool:
    """APIの疎通確認"""
    print(f"[TEST] ポート {port} でAPIテストを実行中...")
    
    try:
        response = requests.post(
            f"http://127.0.0.1:{port}/api/moderation/check",
            headers={
                "Authorization": "Bearer dev-token",
                "Content-Type": "application/json"
            },
            json={
                "content": "テスト",
                "content_type": "post"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("[SUCCESS] APIテスト成功!")
            print(f"レスポンス: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"[ERROR] APIテスト失敗: {response.status_code}")
            print(f"エラー: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] APIテストエラー: {e}")
        return False

def stop_server(process: subprocess.Popen):
    """サーバーを停止"""
    if process and process.poll() is None:
        print("[INFO] サーバーを停止中...")
        try:
            process.terminate()
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        print("[SUCCESS] サーバーが停止しました")

def find_working_port() -> int:
    """利用可能なポートを見つける"""
    for port in range(8000, 8010):
        try:
            response = requests.get(f"http://127.0.0.1:{port}", timeout=1)
            continue
        except:
            return port
    return 8000

def main():
    """メイン処理"""
    print("[START] 自動IAM修正・テスト・再起動スクリプトを開始します...")
    
    # 1. Terraformでインフラを更新
    if not update_terraform_infrastructure():
        print("[ERROR] Terraformの更新に失敗しました")
        return
    
    # 2. IAMポリシーを再アタッチ
    if not reattach_iam_policy():
        print("[ERROR] IAMポリシーの再アタッチに失敗しました")
        return
    
    # 3. IAM権限の反映を待つ
    wait_for_iam_propagation()
    
    # 4. Bedrockモデルのテスト
    if not test_bedrock_models():
        print("[ERROR] Bedrockモデルのテストに失敗しました")
        print("[INFO] モックモードで動作確認を行います...")
        
        # モックモードで起動
        port = find_working_port()
        server_process = start_server(port)
        if server_process:
            try:
                # モックモードでAPIテスト
                env = os.environ.copy()
                env['DEBUG'] = 'True'
                server_process.terminate()
                
                # モックモードで再起動
                server_process = subprocess.Popen(
                    f"python -m uvicorn app.main:app --host 127.0.0.1 --port {port}",
                    shell=True,
                    cwd=os.path.join(os.path.dirname(__file__), '..'),
                    env=env
                )
                
                time.sleep(5)
                if test_api(port):
                    print(f"\n[SUCCESS] モックモードで動作確認完了!")
                    print(f"サーバーはポート {port} で動作中です")
                    print("Ctrl+C で停止できます")
                    
                    try:
                        server_process.wait()
                    except KeyboardInterrupt:
                        print("\n[INFO] ユーザーによって停止されました")
                else:
                    print("[ERROR] モックモードでもAPIテストに失敗しました")
                    
            finally:
                stop_server(server_process)
        return
    
    # 5. 利用可能なポートを見つける
    port = find_working_port()
    print(f"[INFO] 使用ポート: {port}")
    
    # 6. サーバーを起動
    server_process = start_server(port)
    if not server_process:
        print("[ERROR] サーバーの起動に失敗しました")
        return
    
    try:
        # 7. APIテスト
        if test_api(port):
            print("\n[SUCCESS] すべてのテストが成功しました!")
            print(f"サーバーはポート {port} で動作中です")
            print("Ctrl+C で停止できます")
            
            # サーバーを起動したままにする
            try:
                server_process.wait()
            except KeyboardInterrupt:
                print("\n[INFO] ユーザーによって停止されました")
        else:
            print("[ERROR] APIテストに失敗しました")
            
    finally:
        # 8. サーバーを停止
        stop_server(server_process)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] スクリプトが中断されました")
    except Exception as e:
        print(f"[ERROR] 予期しないエラー: {e}")
        sys.exit(1) 