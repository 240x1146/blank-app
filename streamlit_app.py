import streamlit as st
from supabase import create_client, Client

# --- 接続設定（名前だけ呼ぶ） ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💪 筋トレ習慣化トラッカー")

# --- データの取得 ---
response = supabase.table("tools").select("*").order("id").execute()
workouts = response.data

for item in workouts:
    with st.container(border=True):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            name = item.get('menu_name', '種目なし')
            count = item.get('count', 0)
            st.write(f"### {name}")
            st.write(f"現在の回数: **{count}** 回")
        with col2:
            if st.button("＋1回", key=f"btn_{item['id']}"):
                supabase.table("tools").update({"count": count + 1}).eq("id", item["id"]).execute()
                st.rerun()