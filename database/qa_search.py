import os
import pyodbc
from dotenv import load_dotenv
from difflib import SequenceMatcher

# .env ファイルから環境変数を読み込む
load_dotenv()

def create_connection():
    conn_str = os.getenv("AZURE_SQL_CONNECTION_STRING")
    return pyodbc.connect(conn_str)

def search_similar_qa(user_input):
    conn = create_connection()
    cursor = conn.cursor()

    # 🔹 正しいテーブル名に変更（faq → qa_table）
    cursor.execute("SELECT Question, Answer FROM qa_table")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # 🔹 類似度スコアを計算（difflib）
    scored_results = sorted(
        rows,
        key=lambda row: SequenceMatcher(None, user_input, row[0]).ratio(),
        reverse=True
    )

    # 🔹 スコア0.3以上の上位3件を返す
    top_matches = [(q, a) for q, a in scored_results if SequenceMatcher(None, user_input, q).ratio() > 0.3][:3]

    return top_matches
