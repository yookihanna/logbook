import streamlit as st
import pandas as pd
from database import create_table, insert_log, get_all_logs, filter_logs
from datetime import datetime
from export import export_to_excel, export_to_word

# Init DB
create_table()

st.title("📘 Logbook Harian")

# Tabs
tab1, tab2 = st.tabs(["📝 Tambah Log", "📂 Semak & Export"])

# =========================
# Tab 1: Tambah Log
# =========================
with tab1:
    st.subheader("Tambah Aktiviti Harian")
    date = st.date_input("Tarikh", datetime.today())
    time = st.time_input("Masa", datetime.now().time())
    activity = st.text_area("Aktiviti")
    status = st.selectbox("Status", ["Done", "Pending"])

    if st.button("Simpan Log"):
        insert_log(str(date), str(time), activity, status)
        st.success("Log berjaya disimpan!")

# =========================
# Tab 2: Semak & Export
# =========================
with tab2:
    st.subheader("Senarai Aktiviti")

    filter_date = st.date_input("Tapis ikut tarikh", None)
    filter_status = st.selectbox("Tapis ikut status", ["Semua", "Done", "Pending"])

    if filter_status == "Semua":
        logs = filter_logs(date=str(filter_date) if filter_date else None)
    else:
        logs = filter_logs(date=str(filter_date) if filter_date else None, status=filter_status)

    df = pd.DataFrame(logs, columns=["ID", "Tarikh", "Masa", "Aktiviti", "Status"])
    st.dataframe(df, use_container_width=True)

    # Export Buttons
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬇️ Muat Turun Excel"):
                export_to_excel(df)
        with col2:
            if st.button("⬇️ Muat Turun Word"):
                export_to_word(df)
