import requests
import names
import json
import os
from colorama import init, Fore
import time
import random

init(autoreset=True)

print("""
╔═════════════════════════════════════════════╗
║       🌟 LUXURY BOT - Automated Tasks       ║
║     Automate your Luxury Airdrop tasks!     ║
║  Developed by: https://t.me/sentineldiscus  ║
╚═════════════════════════════════════════════╝
""")

REGISTER_URL = "https://luxury-airdrop.onrender.com/api/create-username"
TASK_URL = "https://luxury-airdrop.onrender.com/api/complete-task"
JSON_FILE = "username.json"
PROXY_FILE = "proxy.txt"

TASK_TYPES = [
    "telegramGroup", "telegramChannel", "twitter", "twitterRepost6", "twitterRepost5",
    "twitterRepost4", "twitterRepost3", "twitterRepost2", "twitterRepost1",
    "twitterRetweet", "twitterLike"
]

def load_proxies():
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def get_proxy():
    proxies = load_proxies()
    if proxies:
        proxy = random.choice(proxies)
        return {"http": proxy, "https": proxy}
    return None

def load_usernames():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_username(username, ref_code):
    usernames = load_usernames()
    usernames.append({"username": username, "ref": ref_code})
    with open(JSON_FILE, "w") as f:
        json.dump(usernames, f, indent=4)

def log_message(message, color):
    print(f"{color}{message}")

def register_user(ref_code):
    username = names.get_first_name().lower()
    payload = {
        "username": username,
        "ref": ref_code
    }
    try:
        proxy = get_proxy()
        response = requests.post(REGISTER_URL, json=payload, proxies=proxy)
        if response.status_code == 201:
            log_message(f"ユーザー名 {username} を登録しました", Fore.GREEN)
            save_username(username, ref_code)
            return username
        else:
            log_message(f"ユーザー名 {username} の登録に失敗しました", Fore.RED)
            return None
    except Exception as e:
        log_message(f"登録エラー: {str(e)}", Fore.RED)
        return None

def complete_tasks(username):
    for task in TASK_TYPES:
        payload = {
            "username": username,
            "taskType": task
        }
        try:
            proxy = get_proxy()
            response = requests.post(TASK_URL, json=payload, proxies=proxy)
            if response.status_code == 200:
                log_message(f"{username} のタスク {task} を完了しました", Fore.GREEN)
            else:
                log_message(f"{username} のタスク {task} に失敗しました", Fore.YELLOW)
            time.sleep(60)
        except Exception as e:
            log_message(f"タスク {task} のエラー: {str(e)}", Fore.RED)

def main():
    try:
        num_requests = int(input("リファラル数を入力してください: "))
        ref_code = input("リファラルコードを入力してください: ")
        run_tasks = input("すべてのタスクを実行しますか？ (y/n): ").strip().lower()

        if num_requests <= 0:
            log_message("リファラル数は0より大きくしてください", Fore.RED)
            return

        if run_tasks not in ['y', 'n']:
            log_message("入力は'y'または'n'にしてください", Fore.RED)
            return

        log_message(f"リファラルコード {ref_code} で {num_requests} 件のリクエストを開始します", Fore.GREEN)
        
        for i in range(num_requests):
            log_message(f"リクエスト {i+1} 件目", Fore.YELLOW)
            username = register_user(ref_code)
            if username and run_tasks == 'y':
                complete_tasks(username)
            time.sleep(2)
    except ValueError:
        log_message("リファラル数は数字で入力してください", Fore.RED)
    except Exception as e:
        log_message(f"エラー: {str(e)}", Fore.RED)

if __name__ == "__main__":
    main()
