import requests
import os
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = "law-index"

headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_API_KEY
}

def check_index():
    """
    インデックス内のデータを取得して、確認する
    """
    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{INDEX_NAME}/docs?api-version=2024-07-01&$top=5"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        results = response.json().get("value", [])
        if results:
            print("✅ インデックスに登録されたデータ:\n")
            for result in results:
                print(f"🔹 {result.get('title', 'タイトルなし')} (ID: {result.get('id', 'IDなし')})")
                print(f"📜 法律の内容: {result.get('content', '法律の内容なし')}\n")
        else:
            print("⚠ インデックスは空です！データをアップロードしてください。")
    else:
        print(f"❌ インデックスデータ取得失敗: {response.text}")

if __name__ == "__main__":
    check_index()