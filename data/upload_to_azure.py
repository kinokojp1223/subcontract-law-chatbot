import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")  # Azure AI Searchのエンドポイント
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")  # APIキー
INDEX_NAME = "law-index"  # 作成したインデックス名

# JSONファイルを読み込み
with open("data/parsed_law.json", encoding="utf-8") as f:
    law_data = json.load(f)

headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_API_KEY
}

# データをアップロードするURL
url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{INDEX_NAME}/docs/index?api-version=2024-07-01"

# APIにデータを送信
data = {"value": law_data}
response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("✅ データをAzure AI Searchにアップロードしました！")
else:
    print(f"❌ アップロード失敗: {response.text}")