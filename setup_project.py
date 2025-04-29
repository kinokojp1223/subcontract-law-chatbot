import os

root_folder = "C:/Python/VirtualSandbox2/chatbot_dev/chatbot_project"

folders = [
    f"{root_folder}/app",
    f"{root_folder}/data",
    f"{root_folder}/tests"
]

files = [
    f"{root_folder}/app/__init__.py",
    f"{root_folder}/app/main.py",
    f"{root_folder}/app/bot_logic.py",
    f"{root_folder}/app/search.py",
    f"{root_folder}/app/database.py",
    f"{root_folder}/app/config.py",
    f"{root_folder}/data/faq.json",
    f"{root_folder}/data/law_data.xml",
    f"{root_folder}/tests/test_bot.py",
    f"{root_folder}/tests/test_search.py",
    f"{root_folder}/requirements.txt",
    f"{root_folder}/README.md",
    f"{root_folder}/.env"
]

# フォルダ作成
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# ファイル作成
for file in files:
    open(file, 'w').close()

print("プロジェクト構成が作成されました！")