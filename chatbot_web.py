import streamlit as st
from chatbot import search_law, generate_gpt_response
from database.qa_search import search_similar_qa
from langdetect import detect
from googletrans import Translator

# Streamlitページ設定
st.set_page_config(page_title="下請代金支払遅延等防止法チャットボット", layout="centered")

# 言語切替
lang = st.radio("🌐 Select Language / 言語を選んでください", ["日本語", "English"], horizontal=True)

# タイトル・UIテキスト切り替え
if lang == "日本語":
    st.title("📘 下請代金支払遅延等防止法【下請法】チャットボット")
    st.markdown("自然な言葉で質問してください。")
    placeholder_text = "例: 支払いが60日を超えてしまった場合は？"
    submit_button_text = "📝 質問を入力してください"
    warning_text = "⚠️ このチャットボットは法律の参考情報を提供するものであり、正式な法律アドバイスではありません。詳細は専門家にご相談ください。"
else:
    st.title("📘 Subcontract Act Chatbot")
    st.markdown("Please ask your question in natural English or Japanese.")
    placeholder_text = "e.g., What if the payment is delayed over 60 days?"
    submit_button_text = "📝 Enter your question"
    warning_text = "⚠️ This chatbot provides general information only. For legal advice, please consult a qualified professional."

# 注意書き表示
st.markdown(warning_text)

# ユーザー入力欄
user_input = st.text_input(submit_button_text, placeholder=placeholder_text)

if user_input:
    with st.spinner("考えています..." if lang == "日本語" else "Generating response..."):

        # 🔍 法令データ検索
        law_results = search_law(user_input)

        # 🤖 GPTによる回答生成（lang_hintを明示的に渡す）
        gpt_reply = generate_gpt_response(user_input, law_results, lang_hint=lang)
        if gpt_reply:
            st.subheader("🤖 GPTの回答" if lang == "日本語" else "🤖 GPT's Answer")
            st.write(gpt_reply)

        # 📚 Q&A（Azure Search or DB 検索）
        faq_results = search_similar_qa(user_input, lang_hint=lang)
        st.subheader("📚 よくある質問と回答" if lang == "日本語" else "📚 Frequently Asked Questions")

        if faq_results:
            translator = Translator()
            for q, a in faq_results:
                # 回答文から前後の " を削除
                a = a.strip('"')

                if lang == "English":
                    try:
                        q = translator.translate(q, src="ja", dest="en").text
                        a = translator.translate(a, src="ja", dest="en").text
                    except Exception:
                        pass  # 翻訳エラー時はそのまま表示

                st.markdown(f"**Q: {q}**")
                st.write(f"A: {a}")
        else:
            st.write("📭 類似するQ&Aは見つかりませんでした。" if lang == "日本語" else "📭 No similar Q&A found.")
