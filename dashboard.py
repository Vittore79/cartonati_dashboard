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

st.title("🚨 Centrale Operativa Cartonati")

st.write(
    "Monitoraggio live di news, YouTube e social calcistici"
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

st.sidebar.title("⚙️ Pannello Controllo")

# =========================
# FILTRO TIPO
# =========================

selected_types = st.sidebar.multiselect(

    "Filtra contenuti",

    ["rss", "youtube"],

    default=["rss", "youtube"]
)

# =========================
# RICERCA
# =========================

search_term = st.sidebar.text_input(
    "🔎 Cerca parola chiave"
)

# =========================
# SORGENTI
# =========================

st.sidebar.header("📡 Fonti RSS")

# =========================
# RSS FEEDS
# =========================

st.sidebar.header("📰 Fonti RSS")

rss_feeds = sources.get(
    "rss_feeds",
    []
)

for feed in rss_feeds:

    st.sidebar.write(f"• {feed}")

new_feed = st.sidebar.text_input(
    "Nuovo feed RSS"
)

if st.sidebar.button(
    "➕ Aggiungi feed"
):

    if (
        new_feed
        and new_feed not in rss_feeds
    ):

        rss_feeds.append(new_feed)

        sources["rss_feeds"] = rss_feeds

        with open(
            SOURCES_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                sources,
                file,
                indent=4,
                ensure_ascii=False
            )

        st.sidebar.success(
            "Feed aggiunto!"
        )

        st.rerun()

# =========================
# YOUTUBE
# =========================

st.sidebar.header("🎥 Canali YouTube")

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

# =========================
# GESTIONE KEYWORDS
# =========================

st.sidebar.header("🏷️ Parole Chiave")

keywords = filters.get(
    "important_words",
    []
)

for word in keywords:

    st.sidebar.write(f"• {word}")

new_keyword = st.sidebar.text_input(
    "Nuova keyword"
)

if st.sidebar.button(
    "➕ Aggiungi keyword"
):

    if (
        new_keyword
        and new_keyword not in keywords
    ):

        keywords.append(new_keyword)

        filters["important_words"] = keywords

        with open(
            FILTERS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                filters,
                file,
                indent=4,
                ensure_ascii=False
            )

        st.sidebar.success(
            "Keyword aggiunta!"
        )

        st.rerun()

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

st.header("🚨 Flusso Notizie Live")

for alert in filtered_alerts[:100]:

    with st.container():

        st.subheader(
            alert["titolo"]
        )

        st.write(
            f"📌 Categoria: {alert['tipo']}"
        )

        st.write(
            f"📰 Fonte: {alert['fonte']}"
        )

        st.write(
            f"🕒 Rilevato: {alert['data']}"
        )

        st.markdown(
            f"[🔗 Apri link]({alert['link']})"
        )

        st.divider()