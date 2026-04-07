import streamlit as st
import random

# ─── ページ設定 ───────────────────────────────
st.set_page_config(
    page_title="金銭の問題ドリル",
    page_icon="💰",
    layout="centered"
)

# ─── CSS ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
}

/* ヘッダー */
.app-header {
    background: #d63031;
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.app-header h1 { font-size: 1.3rem; margin: 0; }
.app-header p  { margin: 0; font-size: 0.85rem; opacity: 0.9; }

/* カード */
.card {
    background: white;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

/* レベルバッジ */
.badge-kiso {
    background: #ffeaea; color: #d63031;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    display: inline-block; margin-bottom: 8px;
}
.badge-oyo {
    background: #e8eaf6; color: #1a237e;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    display: inline-block; margin-bottom: 8px;
}

/* 問題文 */
.q-text {
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.8;
    color: #1a1a2e;
}

/* フィードバック */
.fb-correct {
    background: #e8f5ee;
    border-left: 4px solid #2e7d52;
    border-radius: 0 10px 10px 0;
    padding: 14px 16px;
    margin-top: 12px;
}
.fb-wrong {
    background: #ffeaea;
    border-left: 4px solid #d63031;
    border-radius: 0 10px 10px 0;
    padding: 14px 16px;
    margin-top: 12px;
}
.fb-title-ok  { color: #2e7d52; font-weight: 800; font-size: 1rem; margin-bottom: 6px; }
.fb-title-ng  { color: #d63031; font-weight: 800; font-size: 1rem; margin-bottom: 6px; }
.fb-solution  { font-size: 0.88rem; color: #333; line-height: 1.8; }

/* プログレス */
.progress-wrap {
    background: #f0eeea;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 結果 */
.result-score {
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    margin: 12px 0 4px;
}
.result-msg {
    text-align: center;
    font-size: 1rem;
    font-weight: 700;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
}
.review-item {
    border: 1.5px solid #eee;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    background: #fafaf8;
}

/* ボタン上書き */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 700;
    padding: 10px;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# ─── 問題データ ────────────────────────────────
ALL_QUESTIONS = [
    # 基礎
    {
        "level": "基礎",
        "q": "3000円で仕入れた商品に40%の利益を加えた定価はいくらか。",
        "choices": ["4200円", "4600円", "4900円", "5200円", "4400円"],
        "answer": 0,
        "solution": "利益 = 3000 × 0.4 = **1200円**\n\n定価 = 3000 + 1200 = **4200円**"
    },
    {
        "level": "基礎",
        "q": "定価15000円の商品を30%引きで売った。売値はいくらか。",
        "choices": ["11500円", "10500円", "12000円", "11000円", "9000円"],
        "answer": 1,
        "solution": "売値 = 定価 × (1 − 割引率)\n\n= 15000 × (1 − 0.3) = 15000 × **0.7** = **10500円**"
    },
    {
        "level": "基礎",
        "q": "原価1200円の商品を1800円で売った。利益は原価の何%か。",
        "choices": ["40%", "45%", "50%", "30%", "35%"],
        "answer": 2,
        "solution": "利益 = 1800 − 1200 = **600円**\n\n利益率 = 600 ÷ 1200 × 100 = **50%**"
    },
    {
        "level": "基礎",
        "q": "原価6000円の品物に2割5分の利益を見込んで定価をつけた。定価はいくらか。",
        "choices": ["8400円", "7800円", "8700円", "7500円", "8100円"],
        "answer": 3,
        "solution": "2割5分 = **0.25**\n\n利益 = 6000 × 0.25 = 1500円\n\n定価 = 6000 + 1500 = **7500円**"
    },
    {
        "level": "基礎",
        "q": "定価9000円の商品を1割8分引きで売ったときの売値はいくらか。",
        "choices": ["7020円", "6480円", "7200円", "6840円", "7380円"],
        "answer": 4,
        "solution": "1割8分 = **0.18**\n\n売値 = 9000 × (1 − 0.18) = 9000 × 0.82 = **7380円**"
    },
    # 応用
    {
        "level": "応用",
        "q": "原価5000円の商品に3割の利益をのせて定価にした。定価の2割引きで売ったときの利益はいくらか。",
        "choices": ["450円", "700円", "550円", "350円", "200円"],
        "answer": 4,
        "solution": "定価 = 5000 × 1.3 = **6500円**\n\n売値 = 6500 × 0.8 = **5200円**\n\n利益 = 5200 − 5000 = **200円**"
    },
    {
        "level": "応用",
        "q": "ある商品を定価の1割引きで売ると600円の利益があり、2割引きで売ると100円の利益になった。この商品の原価はいくらか。",
        "choices": ["4500円", "3600円", "4200円", "4800円", "3900円"],
        "answer": 0,
        "solution": "定価をPとする。\n\n① 0.9P − 原価 = 600\n\n② 0.8P − 原価 = 100\n\n①−②：0.1P = 500 → P = **5000円**\n\n原価 = 5000 × 0.9 − 600 = **4500円**"
    },
    {
        "level": "応用",
        "q": "定価20000円の商品をセールで16000円で売った。これは定価の何%引きか。",
        "choices": ["35%", "20%", "40%", "25%", "30%"],
        "answer": 1,
        "solution": "値引額 = 20000 − 16000 = **4000円**\n\n割引率 = 4000 ÷ 20000 × 100 = **20%**"
    },
    {
        "level": "応用",
        "q": "原価10000円の品物に4割の利益を見込んで定価をつけたが、売れなかったので定価の2割5分引きで売った。このとき利益は原価の何%か。",
        "choices": ["3%", "4%", "5%", "1%", "2%"],
        "answer": 2,
        "solution": "定価 = 10000 × 1.4 = **14000円**\n\n売値 = 14000 × 0.75 = **10500円**\n\n利益率 = (10500 − 10000) ÷ 10000 × 100 = **5%**"
    },
    {
        "level": "応用",
        "q": "原価10000円の品物に5割の利益をのせて定価をつけた。定価の3割引きで売ったときの利益はいくらか。",
        "choices": ["700円", "800円", "600円", "500円", "900円"],
        "answer": 3,
        "solution": "定価 = 10000 × 1.5 = **15000円**\n\n売値 = 15000 × 0.7 = **10500円**\n\n利益 = 10500 − 10000 = **500円**"
    },
]

LABELS = ["A", "B", "C", "D", "E"]

# ─── セッション初期化 ─────────────────────────
def init_session():
    if "questions" not in st.session_state:
        q = ALL_QUESTIONS.copy()
        random.shuffle(q)
        st.session_state.questions   = q
        st.session_state.current     = 0
        st.session_state.correct     = 0
        st.session_state.wrong_list  = []
        st.session_state.answered    = False
        st.session_state.chosen      = None
        st.session_state.screen      = "start"  # start / quiz / result

def reset_quiz(pool=None):
    q = (pool if pool else ALL_QUESTIONS.copy())
    random.shuffle(q)
    st.session_state.questions  = q
    st.session_state.current    = 0
    st.session_state.correct    = 0
    st.session_state.wrong_list = []
    st.session_state.answered   = False
    st.session_state.chosen     = None
    st.session_state.screen     = "quiz"

init_session()

# ─── ヘッダー ─────────────────────────────────
total = len(st.session_state.get("questions", ALL_QUESTIONS))
done  = st.session_state.get("current", 0)
st.markdown(f"""
<div class="app-header">
  <div>
    <h1>💰 金銭の問題ドリル</h1>
    <p>就職試験対策｜基礎5問・応用5問</p>
  </div>
  <div style="text-align:right">
    <p style="font-size:1.1rem;font-weight:900">{done} / {total}</p>
    <p>問完了</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── プログレスバー ───────────────────────────
if st.session_state.screen != "start":
    st.progress(done / total if total > 0 else 0)
    st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# スタート画面
# ══════════════════════════════════════════════
if st.session_state.screen == "start":
    st.markdown("""
    <div class="card" style="text-align:center">
      <div style="font-size:3rem">🏪</div>
      <h2 style="color:#d63031;margin:10px 0 8px">就職試験対策<br>金銭の問題ドリル</h2>
      <p style="color:#636e72;line-height:1.8">
        定価・原価・利益・売値の計算を練習しよう。<br>
        間違えた問題には解説が表示されます。
      </p>
      <br>
      <span class="badge-kiso">基礎 5問</span>&nbsp;
      <span class="badge-oyo">応用 5問</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("　　スタート！　　", type="primary"):
        reset_quiz()
        st.rerun()

# ══════════════════════════════════════════════
# 問題画面
# ══════════════════════════════════════════════
elif st.session_state.screen == "quiz":
    q   = st.session_state.questions[st.session_state.current]
    idx = st.session_state.current
    lv  = q["level"]

    # 問題カード
    badge_class = "badge-kiso" if lv == "基礎" else "badge-oyo"
    st.markdown(f"""
    <div class="card">
      <span class="{badge_class}">{lv}</span>
      <p style="color:#888;font-size:0.82rem;margin:4px 0 10px">
        問題 {idx+1} / {total}
      </p>
      <p class="q-text">{q['q']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 選択肢ボタン
    if not st.session_state.answered:
        cols = st.columns(1)
        for i, ch in enumerate(q["choices"]):
            if st.button(f"　{LABELS[i]}　{ch}", key=f"choice_{i}"):
                st.session_state.chosen   = i
                st.session_state.answered = True
                if i == q["answer"]:
                    st.session_state.correct += 1
                else:
                    st.session_state.wrong_list.append(q)
                st.rerun()
    else:
        # 答え後：選択肢を色付きで表示
        chosen  = st.session_state.chosen
        correct = q["answer"]
        for i, ch in enumerate(q["choices"]):
            if i == correct and i == chosen:
                st.success(f"✅  {LABELS[i]}　{ch}　← 正解！")
            elif i == correct:
                st.success(f"✅  {LABELS[i]}　{ch}　← 正解")
            elif i == chosen:
                st.error(f"❌  {LABELS[i]}　{ch}　← あなたの選択")
            else:
                st.markdown(f"　　{LABELS[i]}　{ch}")

        # フィードバック
        is_correct = (chosen == correct)
        if is_correct:
            st.markdown(f"""
            <div class="fb-correct">
              <div class="fb-title-ok">✅ 正解！</div>
              <div class="fb-solution">{q['solution'].replace(chr(10), '<br>')
                .replace('**', '<strong>').replace('</strong><strong>', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            sol_html = q['solution']
            # **テキスト** を <strong> に変換
            import re
            sol_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', sol_html)
            sol_html = sol_html.replace('\n', '<br>')
            st.markdown(f"""
            <div class="fb-wrong">
              <div class="fb-title-ng">❌ 不正解　正解は {LABELS[correct]}：{q['choices'][correct]}</div>
              <div class="fb-solution"><strong>【解き方】</strong><br>{sol_html}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 次へ / 結果へ
        next_label = "次の問題へ →" if idx + 1 < total else "結果を見る 🎉"
        if st.button(next_label, type="primary"):
            if idx + 1 < total:
                st.session_state.current  += 1
                st.session_state.answered  = False
                st.session_state.chosen    = None
            else:
                st.session_state.screen = "result"
            st.rerun()

# ══════════════════════════════════════════════
# 結果画面
# ══════════════════════════════════════════════
elif st.session_state.screen == "result":
    correct_n = st.session_state.correct
    wrong_n   = total - correct_n
    pct       = round(correct_n / total * 100)

    # スコア色
    color = "#2e7d52" if pct == 100 else "#d63031" if pct >= 70 else "#e65100" if pct >= 50 else "#636e72"
    emoji = "🎊" if pct == 100 else "👍" if pct >= 70 else "📖" if pct >= 50 else "💪"
    msg   = (
        "パーフェクト！完璧です！" if pct == 100 else
        "よくできました！もう一度チャレンジしよう" if pct >= 70 else
        "チートシートを見直してからもう一度！" if pct >= 50 else
        "基礎から確認しよう。解説をよく読んでね"
    )
    msg_bg = (
        "#e8f5ee" if pct == 100 else
        "#ffeaea" if pct >= 70 else
        "#fff3e0" if pct >= 50 else "#f0eeea"
    )

    st.markdown(f"""
    <div class="card" style="text-align:center">
      <div style="font-size:2rem">🎉 結果発表</div>
      <div class="result-score" style="color:{color}">{pct}点</div>
      <p style="color:#888;margin-bottom:16px">{total}問中 {correct_n}問正解</p>
      <div class="result-msg" style="background:{msg_bg};color:{color}">{emoji} {msg}</div>
      <div style="display:flex;justify-content:center;gap:40px;margin-top:16px">
        <div>
          <div style="font-size:2rem;font-weight:900;color:#2e7d52">{correct_n}</div>
          <div style="font-size:0.78rem;color:#888">正解</div>
        </div>
        <div>
          <div style="font-size:2rem;font-weight:900;color:#d63031">{wrong_n}</div>
          <div style="font-size:0.78rem;color:#888">不正解</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 復習リスト
    if st.session_state.wrong_list:
        st.markdown("### 📋 間違えた問題の復習")
        import re
        for i, wq in enumerate(st.session_state.wrong_list):
            sol = re.sub(r'\*\*(.+?)\*\*', r'\1', wq['solution'])
            st.markdown(f"""
            <div class="review-item">
              <p style="font-size:0.88rem;font-weight:600;margin-bottom:6px">{i+1}. {wq['q']}</p>
              <p style="font-size:0.82rem;color:#2e7d52;font-weight:700;margin-bottom:4px">
                正解：{LABELS[wq['answer']]}　{wq['choices'][wq['answer']]}
              </p>
              <p style="font-size:0.8rem;color:#555;line-height:1.7">{sol.replace(chr(10),'　')}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄　もう一度（全問）", type="primary"):
            reset_quiz()
            st.rerun()
    with col2:
        if st.session_state.wrong_list:
            if st.button("❌　間違いのみ"):
                reset_quiz(pool=st.session_state.wrong_list.copy())
                st.rerun()
