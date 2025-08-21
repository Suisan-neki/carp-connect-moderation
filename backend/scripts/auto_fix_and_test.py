#!/usr/bin/env python3
"""
自動修正・テスト・再起動スクリプト
Bedrockの問題を自動で解決し、サーバーを再起動してテストします
"""

import subprocess
import time
import sys
import os
import signal
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
            timeout=30
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output
    except subprocess.TimeoutExpired:
        return False, "コマンドがタイムアウトしました"
    except Exception as e:
        return False, str(e)

def find_working_port() -> int:
    """利用可能なポートを見つける"""
    for port in range(8000, 8010):
        try:
            response = requests.get(f"http://127.0.0.1:{port}", timeout=1)
            continue
        except:
            return port
    return 8000

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

def main():
    """メイン処理"""
    print("[START] 自動修正・テスト・再起動スクリプトを開始します...")
    
    # 1. Bedrockモデルのテスト
    if not test_bedrock_models():
        print("[ERROR] Bedrockモデルのテストに失敗しました")
        return
    
    # 2. 利用可能なポートを見つける
    port = find_working_port()
    print(f"[INFO] 使用ポート: {port}")
    
    # 3. サーバーを起動
    server_process = start_server(port)
    if not server_process:
        print("[ERROR] サーバーの起動に失敗しました")
        return
    
    try:
        # 4. APIテスト
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
        # 5. サーバーを停止
        stop_server(server_process)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 スクリプトが中断されました")
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        sys.exit(1) 