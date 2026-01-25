import streamlit as st
from supabase import create_client, Client

# --- 1. Supabase 接続設定 ---
# ここは書き換えずにこのままでOKです（Secretsから読み込む設定です）
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💪 筋トレ記録アプリ（腹筋カウンター）")

# --- 2. データの取得（テーブル名 tools に合わせています） ---
response = supabase.table("tools").select("*").order("id").execute()
workouts = response.data

if not workouts:
    st.write("種目がありません。下の入力欄から追加してください。")

for item in workouts:
    with st.container(border=True):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            # menu_name が無い場合を考えて get() を使っています
            name = item.get('menu_name', '名前なし')
            count = item.get('count', 0)
            st.write(f"### {name}")
            st.write(f"現在の回数: **{count}** 回")
        with col2:
            if st.button("＋1回", key=f"btn_{item['id']}"):
                new_count = count + 1
                supabase.table("tools").update({"count": new_count}).eq("id", item["id"]).execute()
                st.rerun()

# --- 3. 新しい種目の追加 ---
st.divider()
with st.expander("新しい種目を追加"):
    new_menu = st.text_input("例：腹筋")
    if st.button("追加"):
        if new_menu:
            supabase.table("tools").insert({"menu_name": new_menu, "count": 0}).execute()
            st.rerun()