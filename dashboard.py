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
# SESSION STATE
# =========================

if "pending_action" not in st.session_state:

    st.session_state.pending_action = None

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

# ======================================================
# RSS FEEDS
# ======================================================

st.sidebar.header("📰 Fonti RSS")

rss_feeds = sources.get(
    "rss_feeds",
    []
)

for index, feed in enumerate(rss_feeds):

    col1, col2 = st.sidebar.columns([4, 1])

    col1.write(feed)

    if col2.button(
        "❌",
        key=f"rss_delete_{index}"
    ):

        st.session_state.pending_action = {

            "type": "delete_rss",

            "value": feed
        }

# aggiunta feed
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

        st.session_state.pending_action = {

            "type": "add_rss",

            "value": new_feed
        }

# ======================================================
# YOUTUBE
# ======================================================

st.sidebar.header("🎥 Canali YouTube")

youtube_channels = sources.get(
    "youtube_channels",
    []
)

for index, channel in enumerate(youtube_channels):

    col1, col2 = st.sidebar.columns([4, 1])

    col1.write(f"• {channel['name']}")

    if col2.button(
        "❌",
        key=f"yt_delete_{index}"
    ):

        st.session_state.pending_action = {

            "type": "delete_yt",

            "value": channel
        }

# aggiunta youtube
new_channel_name = st.sidebar.text_input(
    "Nome canale"
)

new_channel_id = st.sidebar.text_input(
    "ID canale YouTube"
)

if st.sidebar.button(
    "➕ Aggiungi canale"
):

    if (
        new_channel_name
        and new_channel_id
    ):

        st.session_state.pending_action = {

            "type": "add_yt",

            "value": {

                "name": new_channel_name,

                "id": new_channel_id
            }
        }

# ======================================================
# KEYWORDS
# ======================================================

st.sidebar.header("🏷️ Parole Chiave")

keywords = filters.get(
    "important_words",
    []
)

for index, word in enumerate(keywords):

    col1, col2 = st.sidebar.columns([4, 1])

    col1.write(word)

    if col2.button(
        "❌",
        key=f"kw_delete_{index}"
    ):

        st.session_state.pending_action = {

            "type": "delete_kw",

            "value": word
        }

# aggiunta keyword
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

        st.session_state.pending_action = {

            "type": "add_kw",

            "value": new_keyword
        }

# ======================================================
# CONFERMA AZIONI
# ======================================================

if st.session_state.pending_action:

    action = st.session_state.pending_action

    st.sidebar.warning(
        f"Confermi operazione: {action['type']} ?"
    )

    confirm_col1, confirm_col2 = st.sidebar.columns(2)

    # =========================
    # CONFERMA
    # =========================

    if confirm_col1.button(
        "✅ SI"
    ):

        # RSS
        if action["type"] == "add_rss":

            rss_feeds.append(
                action["value"]
            )

        elif action["type"] == "delete_rss":

            rss_feeds.remove(
                action["value"]
            )

        # YOUTUBE
        elif action["type"] == "add_yt":

            youtube_channels.append(
                action["value"]
            )

        elif action["type"] == "delete_yt":

            youtube_channels.remove(
                action["value"]
            )

        # KEYWORDS
        elif action["type"] == "add_kw":

            keywords.append(
                action["value"]
            )

        elif action["type"] == "delete_kw":

            keywords.remove(
                action["value"]
            )

        # salva sources
        sources["rss_feeds"] = rss_feeds

        sources["youtube_channels"] = youtube_channels

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

        # salva filters
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

        st.session_state.pending_action = None

        st.sidebar.success(
            "Operazione completata!"
        )

        st.rerun()

    # =========================
    # ANNULLA
    # =========================

    if confirm_col2.button(
        "❌ NO"
    ):

        st.session_state.pending_action = None

        st.rerun()

# ======================================================
# FILTRA ALERT
# ======================================================

filtered_alerts = []

for alert in alerts:

    if alert["tipo"] not in selected_types:

        continue

    if search_term:

        text = (
            alert["titolo"] +
            " " +
            alert["fonte"]
        ).lower()

        if search_term.lower() not in text:

            continue

    filtered_alerts.append(alert)

# ======================================================
# STATISTICHE
# ======================================================

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

# ======================================================
# LIVE FEED
# ======================================================

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
            f"[🔗 Apri sorgente]({alert['link']})"
        )

        st.divider()