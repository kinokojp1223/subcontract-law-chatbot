import requests
import json
import os
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

# インデックス名を直接指定（FAQ用）
INDEX_NAME = "faq-index"

# JSONファイルの読み込み
# スクリプトのある場所を基準に JSON を読み込む
script_dir = os.path.dirname(os.path.abspath(__file__))
faq_path = os.path.join(script_dir, "faq.json")
with open(faq_path, encoding="utf-8") as f:
    faq_data = json.load(f)

# ヘッダー情報
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_API_KEY
}

# データ送信先のURL
url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{INDEX_NAME}/docs/index?api-version=2024-07-01"

# アップロード用データを整形
data = {"value": faq_data}

# POSTリクエストでデータ送信
response = requests.post(url, headers=headers, json=data)

# 結果の表示
if response.status_code == 200:
    print("✅ FAQ データを Azure Cognitive Search にアップロードしました！")
else:
    print(f"❌ アップロード失敗: {response.status_code}")
    print(response.text)
