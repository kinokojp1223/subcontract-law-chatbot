import pyodbc
import csv
import os
from dotenv import load_dotenv

# .env 読み込み
load_dotenv()

# 接続情報を取得
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('AZURE_SQL_SERVER')};"
    f"DATABASE={os.getenv('AZURE_SQL_DB')};"
    f"UID={os.getenv('AZURE_SQL_USER')};"
    f"PWD={os.getenv('AZURE_SQL_PASSWORD')};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

# CSVファイルパス
csv_path = "FAQ_Data.csv"  # または 'data/FAQ_Data.csv' にある場合は修正

def upload_csv_to_sql():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # テーブル作成（なければ）
        cursor.execute("""
            IF OBJECT_ID('qa_table', 'U') IS NULL
            CREATE TABLE qa_table (
                id INT IDENTITY(1,1) PRIMARY KEY,
                question NVARCHAR(MAX),
                answer NVARCHAR(MAX)
            )
        """)

        # CSV読み込み＆挿入
        with open(csv_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute(
                    "INSERT INTO qa_table (Question, Answer) VALUES (?, ?)",
                    row["Question"], row["Answer"]
                )

        conn.commit()
        print("✅ Q&AのCSVをAzure SQLにアップロードしました！")

    except Exception as e:
        print(f"❌ アップロードエラー: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    upload_csv_to_sql()
