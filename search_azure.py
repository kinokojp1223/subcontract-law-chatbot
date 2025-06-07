import requests
import json
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# Azure AI Search の設定
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = "law-index"

# HTTPリクエスト用のヘッダー
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_API_KEY
}

def search_azure(query, top=5):
    """
    Azure AI Search にクエリを送信し、検索結果を取得する
    :param query: 検索するキーワード（例: "法律"）
    :param top: 取得する最大件数（デフォルトは5件）
    :return: 検索結果のリスト
    """
    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{INDEX_NAME}/docs/search?api-version=2024-07-01"

    data = {
        "search": f"\"{query}\" OR {query} AND 下請法",
        "top": top
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print(f"❌ 検索失敗: {response.text}")
        return []

# 🔹 スクリプトを直接実行する場合
if __name__ == "__main__":
    query = input("🔍 検索ワードを入力してください: ")
    results = search_azure(query)

    print("\n✅ 検索結果:\n")
    for result in results:
        print(f"🔹 {result['title']} (ID: {result['id']}, Score: {result['@search.score']})")