import streamlit as st
import json
import os

# ======================================================
# CONFIG PAGINA
# ======================================================

st.set_page_config(
    page_title="Cartonati Alert",
    layout="wide"
)

# ======================================================
# FILE
# ======================================================

ALERTS_FILE = "alerts.json"
FILTERS_FILE = "config/filters.json"
SOURCES_FILE = "config/sources.json"

# ======================================================
# SESSION STATE
# ======================================================

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

if "keyword_input_value" not in st.session_state:
    st.session_state.keyword_input_value = ""

if "rss_input_value" not in st.session_state:
    st.session_state.rss_input_value = ""

if "yt_name_input_value" not in st.session_state:
    st.session_state.yt_name_input_value = ""

if "yt_id_input_value" not in st.session_state:
    st.session_state.yt_id_input_value = ""

# ======================================================
# FUNZIONI
# ======================================================

def load_json(path, default):

    if os.path.exists(path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return default


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

# ======================================================
# CARICAMENTO DATI
# ======================================================

alerts = load_json(
    ALERTS_FILE,
    []
)

filters = load_json(
    FILTERS_FILE,
    {}
)

sources = load_json(
    SOURCES_FILE,
    {}
)

# ======================================================
# DEFAULT STRUCTURE
# ======================================================

if "important_words" not in filters:
    filters["important_words"] = []

if "rss_feeds" not in sources:
    sources["rss_feeds"] = []

if "youtube_channels" not in sources:
    sources["youtube_channels"] = []

# ======================================================
# HEADER
# ======================================================

st.title("🚨 Centrale Operativa Cartonati")

st.write(
    "Monitoraggio live di news, YouTube e social calcistici"
)

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("⚙️ Pannello Controllo")

# ======================================================
# FILTRI
# ======================================================

selected_types = st.sidebar.multiselect(

    "Filtra contenuti",

    ["rss", "youtube"],

    default=["rss", "youtube"]
)

search_term = st.sidebar.text_input(
    "🔎 Cerca parola chiave"
)

# ======================================================
# RSS FEEDS
# ======================================================

st.sidebar.header("📰 Fonti RSS")

for index, feed in enumerate(
    sources["rss_feeds"]
):

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

# ======================================================
# INPUT RSS
# ======================================================

new_feed = st.sidebar.text_input(

    "Nuovo feed RSS",

    value=st.session_state.rss_input_value,

    key="rss_widget"
)

st.session_state.rss_input_value = new_feed

# ======================================================
# BOTTONE RSS
# ======================================================

if st.sidebar.button(
    "➕ Aggiungi feed"
):

    if (
        new_feed
        and new_feed not in sources["rss_feeds"]
    ):

        st.session_state.pending_action = {

            "type": "add_rss",

            "value": new_feed
        }

# ======================================================
# YOUTUBE CHANNELS
# ======================================================

st.sidebar.header("🎥 Canali YouTube")

for index, channel in enumerate(
    sources["youtube_channels"]
):

    col1, col2 = st.sidebar.columns([4, 1])

    col1.write(
        f"• {channel['name']}"
    )

    if col2.button(
        "❌",
        key=f"yt_delete_{index}"
    ):

        st.session_state.pending_action = {

            "type": "delete_yt",

            "value": channel
        }

# ======================================================
# INPUT YOUTUBE
# ======================================================

new_channel_name = st.sidebar.text_input(

    "Nome canale",

    value=st.session_state.yt_name_input_value,

    key="yt_name_widget"
)

st.session_state.yt_name_input_value = (
    new_channel_name
)

new_channel_id = st.sidebar.text_input(

    "ID canale YouTube",

    value=st.session_state.yt_id_input_value,

    key="yt_id_widget"
)

st.session_state.yt_id_input_value = (
    new_channel_id
)

# ======================================================
# BOTTONE YOUTUBE
# ======================================================

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

for index, word in enumerate(
    filters["important_words"]
):

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

# ======================================================
# INPUT KEYWORD
# ======================================================

new_keyword = st.sidebar.text_input(

    "Nuova keyword",

    value=st.session_state.keyword_input_value,

    key="keyword_widget"
)

st.session_state.keyword_input_value = (
    new_keyword
)

# ======================================================
# BOTTONE KEYWORD
# ======================================================

if st.sidebar.button(
    "➕ Aggiungi keyword"
):

    if (
        new_keyword
        and new_keyword not in filters["important_words"]
    ):

        st.session_state.pending_action = {

            "type": "add_kw",

            "value": new_keyword
        }

# ======================================================
# CONFERMA OPERAZIONI
# ======================================================

if st.session_state.pending_action:

    action = st.session_state.pending_action

    message = "Confermi operazione?"

    # ==================================================
    # KEYWORDS
    # ==================================================

    if action["type"] == "add_kw":

        message = (
            f"Confermi aggiunta keyword: "
            f"{action['value']} ?"
        )

    elif action["type"] == "delete_kw":

        message = (
            f"Confermi eliminazione keyword: "
            f"{action['value']} ?"
        )

    # ==================================================
    # RSS
    # ==================================================

    elif action["type"] == "add_rss":

        message = (
            "Confermi aggiunta feed RSS?"
        )

    elif action["type"] == "delete_rss":

        message = (
            "Confermi eliminazione feed RSS?"
        )

    # ==================================================
    # YOUTUBE
    # ==================================================

    elif action["type"] == "add_yt":

        message = (
            f"Confermi aggiunta canale: "
            f"{action['value']['name']} ?"
        )

    elif action["type"] == "delete_yt":

        message = (
            f"Confermi eliminazione canale: "
            f"{action['value']['name']} ?"
        )

    st.sidebar.warning(message)

    confirm_col1, confirm_col2 = st.sidebar.columns(2)

    # ==================================================
    # CONFERMA
    # ==================================================

    if confirm_col1.button(
        "✅ SI"
    ):

        # RSS
        if action["type"] == "add_rss":

            sources["rss_feeds"].append(
                action["value"]
            )

            st.session_state.rss_input_value = ""

        elif action["type"] == "delete_rss":

            sources["rss_feeds"].remove(
                action["value"]
            )

        # YOUTUBE
        elif action["type"] == "add_yt":

            sources["youtube_channels"].append(
                action["value"]
            )

            st.session_state.yt_name_input_value = ""
            st.session_state.yt_id_input_value = ""

        elif action["type"] == "delete_yt":

            sources["youtube_channels"].remove(
                action["value"]
            )

        # KEYWORDS
        elif action["type"] == "add_kw":

            filters["important_words"].append(
                action["value"]
            )

            st.session_state.keyword_input_value = ""

        elif action["type"] == "delete_kw":

            filters["important_words"].remove(
                action["value"]
            )

        # ==================================================
        # SALVA FILE
        # ==================================================

        save_json(
            SOURCES_FILE,
            sources
        )

        save_json(
            FILTERS_FILE,
            filters
        )

        # ==================================================
        # RESET AZIONE
        # ==================================================

        st.session_state.pending_action = None

        st.sidebar.success(
            "Operazione completata!"
        )

        st.rerun()

    # ==================================================
    # ANNULLA
    # ==================================================

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

    if (
        alert["tipo"]
        not in selected_types
    ):

        continue

    if search_term:

        text = (

            alert["titolo"]

            + " "

            + alert["fonte"]

        ).lower()

        if (
            search_term.lower()
            not in text
        ):

            continue

    filtered_alerts.append(alert)

# ======================================================
# STATISTICHE
# ======================================================

st.header("📊 Statistiche")

total_alerts = len(
    filtered_alerts
)

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

st.header(
    "🚨 Flusso Notizie Live"
)

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