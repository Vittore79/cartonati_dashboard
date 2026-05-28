import streamlit as st
import json
import os
import pandas as pd

# =========================
# CONFIG PAGINA
# =========================

st.set_page_config(
    page_title="Cartonati Alert",
    layout="wide"
)

# =========================
# TITOLO
# =========================

st.title("🚨 Cartonati Alert Dashboard")

st.write(
    "Monitoraggio live news, YouTube e social"
)

# =========================
# FILE JSON
# =========================

JSON_FILE = "alerts.json"

# =========================
# CONTROLLO FILE
# =========================

if not os.path.exists(JSON_FILE):

    st.error(
        "alerts.json non trovato"
    )

    st.stop()

# =========================
# CARICA ALERT
# =========================

with open(
    JSON_FILE,
    "r",
    encoding="utf-8"
) as file:

    alerts = json.load(file)

# =========================
# NESSUN ALERT
# =========================

if not alerts:

    st.warning(
        "Nessun alert trovato."
    )

    st.stop()

# =========================
# STATISTICHE
# =========================

st.header("📊 Statistiche")

total_alerts = len(alerts)

youtube_alerts = len([
    a for a in alerts
    if a["tipo"] == "youtube"
])

rss_alerts = len([
    a for a in alerts
    if a["tipo"] == "rss"
])

col1, col2, col3 = st.columns(3)

col1.metric(
    "Totale Alert",
    total_alerts
)

col2.metric(
    "YouTube",
    youtube_alerts
)

col3.metric(
    "RSS News",
    rss_alerts
)

# =========================
# ULTIMI ALERT
# =========================

st.header("🚨 Ultimi Alert")

for alert in alerts[:50]:

    with st.container():

        st.subheader(
            alert["titolo"]
        )

        st.write(
            f"📌 Tipo: {alert['tipo']}"
        )

        st.write(
            f"📰 Fonte: {alert['fonte']}"
        )

        st.write(
            f"🕒 Data: {alert['data']}"
        )

        st.markdown(
            f"[🔗 Apri link]({alert['link']})"
        )

        st.divider()