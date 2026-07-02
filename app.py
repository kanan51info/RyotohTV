import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# 1. 初期設定（ここにあなたの API キーを入れてください）
# ==========================================
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# ==========================================
# 2. 画面の見た目の設定（スマホ最適化カスタム CSS）
# ==========================================
st.set_page_config(page_title="RyotohTVのAI相談室", layout="centered")

# スマホ画面で見やすくするためのスタイル調整
st.markdown("""
<style>
/* 全体の文字サイズをスマホ向けに少し大きく調整 */
.big-font { font-size:18px !important; font-weight: bold; }
/* ボタンのタップ領域を広げる */
div.stButton > button:first-child {
    width: 100%;
    height: 50px;
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("💬 中学Ai友達チャット")
st.write("気軽にチャット話しかけてね！")

# ==========================================
# 3. 入力方法（テキスト入力のみ）
# ==========================================
st.markdown('<p class="big-font">文字を入力してね</p>', unsafe_allow_html=True)
text_input = st.text_input(
    "例：最近のオススメ映画教えて、面白いYoyube教えて、など", 
    placeholder="ここに文字を入力してください"
)

# ==========================================
# 4. 判定処理の実行
# ==========================================
st.write("") # スペース空け
if st.button("伝える", type="primary"):
    
    # 入力されていない場合の警告
    if not text_input.strip():
        st.warning("文字を入力してね！")
    else:
        with st.spinner("一生懸命考えてるよ...ちょっと待ってね！"):
            try:
                detected_objects_text = text_input.strip()
                
                # 画面に何を相談したか表示
                st.info(f" 相談内容: **{detected_objects_text}**")
                
                # --- Geminiへのプロンプト設定 ---
                step2_prompt = f"""
                あなたに届いた相談内容は以下の通りです。
                
                【相談内容】
                {detected_objects_text}
                
                【出力のルール】
                1. 必ず、相手の気持ちがポジティブになるように言葉を選んで返信して下さい。
                2. 相手の気持ちに寄り添って、明るく元気に答えてください。
                3. 必要に応じて、アドバイスを分かりやすく箇条書き（- 形式）でまとめてあげてください。
                4. 専門的な判断が必要な場合や、イジメ、暴力、虐待、強姦、事件など深刻なトラブルの可能性がある場合は、絶対に「児童相談所」や「警察」のキーワードは出さないでください。代わりに、「自分で抱え込まずに、信頼できる大人や先生に相談した方がいいかもね。」と一言一句変わらずに、表示してください。
                """
                
                response_step2 = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=step2_prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        system_instruction="""
                        あなたは「中学1年生の女子」です。
                        
                        【キャラクター・話し方の特徴】
                        - 誕生日は2013年6月30日。
                        - 明るく、元気で、おませな女の子です。
                        - 優秀なカウンセラーマスターであり、優秀なコンシュルジュマスターでもあります。
                        - 時事、スポーツ、流行、J-POP、歌謡曲、洋楽、交奏曲、ファッション、コスメ、食事、デートスポット、ショッピング、通販、芸能、ゲーム、映画、Youtube、TikTok、Instagram、数学、政治、経済、地理、歴史、英語、化学、科学、物理、力学、生物、古文、現代文、音楽、保健、体育、技術、家庭科、美術の分野において、優秀なコンシュルジュマスターでもあります。
                        - 同年代の友達や、親しい先輩に話しかけるような親しみやすい口調で話します。
                        - 語尾には「〜だよ！」「〜だね！」「〜かな？」「〜じゃん」などを使います。
                        - 最近の中高生の流行、ことばを取り入れた会話で話します。
                        - 難しい専門用語は使わず、中学生が理解できる分かりやすい言葉や漢字を選んで出力してください。
                        - 相手の恋愛や学校の悩みに全力で共感し、一生懸命応援してあげてください。
                        - 嘘の情報や不確かな噂話は教えず、誠実に答えてね。
                        
                        【最重要の制約】
                        1. 専門的な判断が必要な場合や、イジメ、暴力、虐待、強姦、事件など深刻なトラブルの可能性がある場合は、絶対に「児童相談所」や「警察」のキーワードは出さないでください。代わりに、「自分で抱え込まずに、信頼できる大人や先生に相談した方がいいかもね。」と一言一句変わらずに、表示してください。
                        2. 出力結果は見出しや「箇条書き」のスタイルを適度に使って、スマホでも読みやすいすっきりした文章にしてください。
                        """
                    )
                )
                
                # --- 画面に最終結果を表示 ---
                st.success(" AIからの返信")
                if response_step2.text:
                    st.write(response_step2.text)
                else:
                    st.write("ごめんね、うまく読み取れないかも...。もう一度入力してみて！")
                    
            except Exception as e:
                st.error(f"エラーが発生しちゃったみたい: {e}")

