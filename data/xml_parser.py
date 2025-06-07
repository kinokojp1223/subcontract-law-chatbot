import xml.etree.ElementTree as ET
import json

# XMLデータを解析してJSONに変換する関数
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    laws = []

    for law in root.findall(".//Article"):
        law_data = {
            "id": law.get("Num"),
            "title": law.find("ArticleTitle").text,
            "content": "".join([p.text for p in law.findall("Paragraph/ParagraphSentence/Sentence") if p.text])
        }
        laws.append(law_data)

    return laws

# XMLファイルを読み込んで変換
xml_file = "chatbot_project/data/law_data.xml"  
law_json = parse_xml(xml_file)

# JSONファイルとして保存
with open("chatbot_project/data/parsed_law.json", "w", encoding="utf-8") as f:
    json.dump(law_json, f, ensure_ascii=False, indent=4)

print("✅ XMLデータをJSONに変換しました！")