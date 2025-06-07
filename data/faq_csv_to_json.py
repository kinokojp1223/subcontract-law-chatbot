import csv
import json

input_csv = "../FAQ_Data.csv"  # 1階層上にあるCSVファイルを参照
output_json = "faq.json"       # 同じフォルダ内に出力


faqs = []

with open(input_csv, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        faq = {
            "id": row["Q No."].strip(),
            "question": row["Question"].strip(),
            "answer": row["Answer"].strip().strip('"'),
            "article": row["Article"].strip(),
            "category_level_1": row["Category Level 1"].strip(),
            "category_level_2": row["Category Level 2"].strip(),
            "category_level_3": row["Category Level 3"].strip()
        }
        faqs.append(faq)

with open(output_json, "w", encoding="utf-8") as jsonfile:
    json.dump(faqs, jsonfile, ensure_ascii=False, indent=2)

print("✅ FAQ データを JSON に変換しました！")
