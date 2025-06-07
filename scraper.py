import csv
import re
from bs4 import BeautifulSoup

# ファイルのパス
html_filename = "sitauke_qa.html"
csv_filename = "FAQ_Data_Cleaned.csv"

# CSVヘッダー
csv_headers = ["Category Level 1", "Category Level 2", "Category Level 3", "Question", "Answer", "Article", "Q No."]

faq_data = []

# ファイルを開いて289行目以降を取得
with open(html_filename, "r", encoding="utf-8") as file:
    lines = file.readlines()  # すべての行を取得
    target_html = "\n".join(lines[288:])  # 289行目以降を結合（0-indexのため288）

# BeautifulSoupを使ってHTMLを解析
soup = BeautifulSoup(target_html, "html.parser")

# すべてのタグを削除してテキスト化
clean_text = soup.get_text(separator="\n").strip()

# 不要な特殊文字を正規表現で削除
clean_text = re.sub(r'\s+', ' ', clean_text)  # 余分なスペース削除
clean_text = re.sub(r'[\r\n]+', '\n', clean_text)  # 余分な改行削除

# 改行で分割してリスト化
lines = clean_text.split("\n")

# 整理されたFAQデータを格納
for line in lines:
    faq_data.append([line.strip()])  # 空白を削除してリストに追加

# CSVファイルに書き込み
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)  # ヘッダーを書き込み
    writer.writerows(faq_data)  # データを書き込み

print(f"✅ 不要なHTMLデータを削除して {csv_filename} に保存しました！")