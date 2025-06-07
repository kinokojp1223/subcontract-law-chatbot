import os
import pyodbc
from dotenv import load_dotenv
from difflib import SequenceMatcher
from googletrans import Translator  # pip install googletrans==4.0.0-rc1

# 環境変数の読み込み
load_dotenv()

# 翻訳用インスタンス
translator = Translator()


def create_connection():
    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DB")
    username = os.getenv("AZURE_SQL_USER")
    password = os.getenv("AZURE_SQL_PASSWORD")

    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )

    return pyodbc.connect(conn_str)


def search_similar_qa(user_input, lang_hint="auto"):
    # 言語判定：UI からのヒントを優先（誤検出回避）
    if lang_hint == "日本語":
        lang = "ja"
    elif lang_hint == "English":
        lang = "en"
    else:
        from langdetect import detect
        try:
            lang = detect(user_input)
        except:
            lang = "ja"

    # 英語なら翻訳して検索に使う
    translated_input = user_input
    if lang != "ja":
        try:
            translated_input = translator.translate(user_input, src=lang, dest="ja").text
        except:
            pass

    # データベース接続・取得
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Question, Answer FROM qa_table")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # 類似度スコアを計算して上位3件取得
    scored_results = sorted(
        rows,
        key=lambda row: SequenceMatcher(None, translated_input, row[0]).ratio(),
        reverse=True
    )

    top_matches = []
    for q, a in scored_results:
        score = SequenceMatcher(None, translated_input, q).ratio()
        if translated_input in q:
            score += 0.3  # 質問に単語が含まれていれば加点

        if score > 0.3:
            if lang != "ja":
                try:
                    q_translated = translator.translate(q, src="ja", dest=lang).text
                    a_translated = translator.translate(a, src="ja", dest=lang).text
                    top_matches.append((q_translated, a_translated))
                except:
                    top_matches.append((q, a))
            else:
                top_matches.append((q, a))

        if len(top_matches) >= 3:
            break

    return top_matches
