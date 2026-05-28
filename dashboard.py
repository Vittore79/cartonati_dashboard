import streamlit as st
import os

st.set_page_config(
    page_title="Cartonati Alert",
    layout="wide"
)

st.title("🚨 Cartonati Alert Dashboard")

st.write("Sistema monitoraggio news e social")

# =========================
# NEWS INVIATE
# =========================

st.header("📨 Contenuti inviati")

if os.path.exists("sent_news.txt"):

    with open(
        "sent_news.txt",
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    if lines:

        for line in reversed(lines[-100:]):

            st.text(line.strip())

    else:

        st.warning(
            "Nessun contenuto trovato."
        )

else:

    st.error(
        "sent_news.txt non trovato."
    )