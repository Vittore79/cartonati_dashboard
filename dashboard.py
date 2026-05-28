import streamlit as st
import json
import os

# =========================
# CONFIG PAGINA
# =========================

st.set_page_config(
    page_title="Cartonati Alert",
    layout="wide"
)

# =========================
# FILE
# =========================

ALERTS_FILE = "alerts.json"

FILTERS_FILE = "config/filters.json"

SOURCES_FILE = "config/sources.json"

# =========================
# TITOLO
# =========================

st.title("🚨 Cartonati Alert Dashboard")

st.write(
    "Monitoraggio live news, YouTube e social"
)

# =========================
# CARICA ALERT
# =========================

if not os.path.exists(ALERTS_FILE):

    st.error(
        "alerts.json non trovato"
    )

    st.stop()

with open(
    ALERTS_FILE,
    "r",
    encoding="utf-8"
) as file:

    alerts = json.load(file)

# =========================
# CARICA FILTERS
# =========================

if os.path.exists(FILTERS_FILE):

    with open(
        FILTERS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        filters = json.load(file)

else:

    filters = {}

# =========================
# CARICA SOURCES
# =========================

if os.path.exists(SOURCES_FILE):

    with open(
        SOURCES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        sources = json.load(file)

else:

    sources = {}

# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙️ Controlli")

# =========================
# FILTRO TIPO
# =========================

selected_types = st.sidebar.multiselect(

    "Filtra per tipo",

    ["rss", "youtube"],

    default=["rss", "youtube"]
)

# =========================
# RICERCA
# =========================

search_term = st.sidebar.text_input(
    "🔎 Cerca keyword"
)

# =========================
# SORGENTI
# =========================

st.sidebar.header("📡 RSS Feeds")

for feed in sources.get(
    "rss_feeds",
    []
):

    st.sidebar.write(
        f"• {feed}"
    )

# =========================
# YOUTUBE
# =========================

st.sidebar.header("🎥 YouTube")

for channel in sources.get(
    "youtube_channels",
    []
):

    st.sidebar.write(
        f"• {channel['name']}"
    )

# =========================
# FILTRI
# =========================

st.sidebar.header("🏷️ Keywords")

for word in filters.get(
    "important_words",
    []
):

    st.sidebar.write(
        f"• {word}"
    )

# =========================
# FILTRA ALERT
# =========================

filtered_alerts = []

for alert in alerts:

    # filtro tipo
    if alert["tipo"] not in selected_types:

        continue

    # ricerca keyword
    if search_term:

        text = (
            alert["titolo"] +
            " " +
            alert["fonte"]
        ).lower()

        if search_term.lower() not in text:

            continue

    filtered_alerts.append(alert)

# =========================
# STATISTICHE
# =========================

st.header("📊 Statistiche")

total_alerts = len(filtered_alerts)

youtube_alerts = len([
    a for a in filtered_alerts
    if a["tipo"] == "youtube"
])

rss_alerts = len([
    a for a in filtered_alerts
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
# ALERT
# =========================

st.header("🚨 Live Feed")

for alert in filtered_alerts[:100]:

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