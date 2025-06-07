import requests
import json
import os
import openai
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# Azure AI Search 設定
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = os.getenv("FAQ_INDEX_NAME", "law-index")  # デフォルトを law-index に

# Azure OpenAI 設定
openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# ヘッダー設定
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_API_KEY
}

# 🔍 法令検索
def search_law(query):
    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{INDEX_NAME}/docs/search?api-version=2024-07-01"
    search_query = f"\"{query}\" OR {query} AND 下請法"
    data = {
        "search": search_query,
        "select": "id,title,content",
        "top": 3
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        results = response.json().get("value", [])
        return results if isinstance(results, list) else []
    else:
        print(f"❌ 検索失敗: {response.text}")
        return []

# 🤖 GPTで回答生成（UI側から言語ヒントを受け取って制御）
def generate_gpt_response(user_input, law_results, lang_hint="日本語"):
    law_text = "\n\n".join([f"{r['title']}\n{r['content']}" for r in law_results])

    if lang_hint == "日本語":
        prompt = f"""
あなたは下請法に詳しい法律アドバイザーです。
以下の質問に対して、下請法に違反するかどうかを判断し、その理由や参考となる条文と共に日本語でわかりやすく答えてください。

【質問】
{user_input}

【関連する法律情報】
{law_text}
"""
    else:
        prompt = f"""
You are a legal expert in Japan's Subcontract Act.
Please explain in clear English whether the following situation violates the law.
Include relevant reasoning and references to specific articles of the Subcontract Act.

[Question]
{user_input}

[Relevant Legal Information]
{law_text}
"""

    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": "You are a legal advisor who explains the Japanese Subcontract Act."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message["content"].strip()

# 📘 条文の要約（やさしい日本語）
def summarize_law_text(text):
    prompt = f"次の法律の条文を初心者にもわかりやすくやさしい日本語で説明してください：\n\n{text}"

    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": "あなたは法律をやさしく説明するアシスタントです。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message["content"].strip()
