import streamlit as st
from supabase import create_client, Client

# --- 1. Supabase 接続設定 ---
# ここに直接URLを書くとエラーになりやすいため、Secretsから読み込みます
url: str = st.secrets["https://kjlxlxvcdqsxoyzqntdr.supabase.co"]
key: str = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqbHhseHZjZHFzeG95enFudGRyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzNDI1OTQsImV4cCI6MjA4NDkxODU5NH0.A5xUYu0fu9joRvUornHOc6coWOXp1D8_uPqUaVwEZZc"

]
supabase: Client = create_client(url, key)

st.title("💪 筋トレ記録アプリ（腹筋カウンター）")

# --- 2. データの取得 ---
response = supabase.table("tools").select("*").order("id").execute()
workouts = response.data

for item in workouts:
    with st.container(border=True):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
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