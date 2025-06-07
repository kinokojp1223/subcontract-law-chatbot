# 1️⃣ 必要なライブラリのインポート
import pandas as pd
import pyodbc
from azure.storage.blob import BlobServiceClient

# 2️⃣ 接続情報の設定
STORAGE_ACCOUNT_NAME = "stractestjp05161655hs"
STORAGE_ACCOUNT_KEY = "jnIRC+/WbbVQI4PuUZCOwZcP9aLUL7uFrw8vcIG3xAj5L+Ymb17k28Z7zWVg2XP+zPwlRUYG3E33+ASt3Wrpxg=="
CONTAINER_NAME = "faq-data-storage"
BLOB_NAME = "TheSubcontractAct.csv"

# SQL Server 接続情報
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=tcp:free-sql-mi-2638472.42b1a81f5c85.database.windows.net,1433;'
    'DATABASE=faq_database;'
    'UID=your-username;'
    'PWD=your-password;'
    'Encrypt=Yes;'  # ここを修正！
    'TrustServerCertificate=No;'
    'Connection Timeout=60;'
)

# 3️⃣ BlobからCSVファイルを取得
blob_service_client = BlobServiceClient(account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=STORAGE_ACCOUNT_KEY)
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
blob_data = blob_client.download_blob().readall()

# 4️⃣ CSVデータを解析・インポート
df = pd.read_csv(pd.io.common.BytesIO(blob_data), encoding="utf-8")
for index, row in df.iterrows():
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subcontract_law_qa (id, question, answer) VALUES (?, ?, ?)",
        row["id"], row["question"], row["answer"]
    )
    conn.commit()

# 5️⃣ 接続を閉じる
conn.close()
print("データインポート完了！")