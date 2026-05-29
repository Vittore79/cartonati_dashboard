import streamlit as st
import json
import os
import re
import subprocess
import requests
import sys
from datetime import datetime

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

    try:

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

        st.success(f"Salvato: {path}")

    except Exception as error:

        st.error(
            f"Errore salvataggio: {error}"
        )

# ======================================================
# CARICA DATI
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
# CONTROLLO MANUALE
# ======================================================

st.divider()

last_update = datetime.now().strftime(
    "%d/%m/%Y %H:%M:%S"
)

col1, col2 = st.columns([3, 1])

with col1:

    st.info(
        f"🕒 Ultimo controllo dashboard: {last_update}"
    )

with col2:

    if st.button(
        "🔄 Avvia scansione"
    ):

        with st.spinner(
            "Scansione in corso..."
        ):

            try:

                result = subprocess.run(

                    [sys.executable, "main.py"],

                    capture_output=True,

                    text=True
                )

                # ==================================================
                # DEBUG OUTPUT
                # ==================================================

                st.subheader(
                    "📄 Output scansione"
                )

                st.code(
                    result.stdout
                )

                st.subheader(
                    "⚠️ Errori"
                )

                st.code(
                    result.stderr
                )

                # ==================================================
                # RISULTATO
                # ==================================================

                if result.returncode == 0:

                    st.success(
                        "✅ Scansione completata!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Errore durante scansione"
                    )

            except Exception as error:

                st.error(
                    f"Errore scansione: {error}"
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

with st.sidebar.expander(
    "📰 Fonti RSS",
    expanded=False
):

    for index, feed in enumerate(
        sources["rss_feeds"]
    ):

        col1, col2 = st.columns([4, 1])

        col1.write(feed)

        if col2.button(
            "❌",
            key=f"rss_delete_{index}"
        ):

            st.session_state.pending_action = {

                "type": "delete_rss",

                "value": feed
            }

    # ==================================================
    # FORM RSS
    # ==================================================

    with st.form(
        "rss_form",
        clear_on_submit=True
    ):

        new_feed = st.text_input(
            "Nuovo feed RSS"
        )

        submit_feed = st.form_submit_button(
            "➕ Aggiungi feed"
        )

        if submit_feed:

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

with st.sidebar.expander(
    "🎥 Canali YouTube",
    expanded=False
):

    for index, channel in enumerate(
        sources["youtube_channels"]
    ):

        col1, col2 = st.columns([4, 1])

        channel_link = channel.get(
            "link",
            "#"
        )

        col1.markdown(
            f"• [{channel['name']}]({channel_link})"
        )

        if col2.button(
            "❌",
            key=f"yt_delete_{index}"
        ):

            st.session_state.pending_action = {

                "type": "delete_yt",

                "value": channel
            }

    # ==================================================
    # FORM YOUTUBE
    # ==================================================

    with st.form(
        "youtube_form",
        clear_on_submit=True
    ):

        youtube_link = st.text_input(
            "Link canale YouTube"
        )

        submit_channel = st.form_submit_button(
            "➕ Aggiungi canale"
        )

        if submit_channel:

            if youtube_link:

                channel_name = youtube_link

                match = re.search(
                    r'@([A-Za-z0-9_\-]+)',
                    youtube_link
                )

                if match:

                    channel_name = (
                        match.group(1)
                    )

                st.session_state.pending_action = {

                    "type": "add_yt",

                    "value": {

                        "name": channel_name,

                        "link": youtube_link
                    }
                }

# ======================================================
# KEYWORDS
# ======================================================

with st.sidebar.expander(
    "🏷️ Parole Chiave",
    expanded=False
):

    for index, word in enumerate(
        filters["important_words"]
    ):

        col1, col2 = st.columns([4, 1])

        col1.write(word)

        if col2.button(
            "❌",
            key=f"kw_delete_{index}"
        ):

            st.session_state.pending_action = {

                "type": "delete_kw",

                "value": word
            }

    # ==================================================
    # FORM KEYWORDS
    # ==================================================

    with st.form(
        "keyword_form",
        clear_on_submit=True
    ):

        new_keyword = st.text_input(
            "Nuova keyword"
        )

        submit_keyword = st.form_submit_button(
            "➕ Aggiungi keyword"
        )

        if submit_keyword:

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

    elif action["type"] == "add_rss":

        message = (
            "Confermi aggiunta feed RSS?"
        )

    elif action["type"] == "delete_rss":

        message = (
            "Confermi eliminazione feed RSS?"
        )

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

    if confirm_col1.button(
        "✅ SI"
    ):

        if action["type"] == "add_rss":

            sources["rss_feeds"].append(
                action["value"]
            )

        elif action["type"] == "delete_rss":

            sources["rss_feeds"].remove(
                action["value"]
            )

        elif action["type"] == "add_yt":

            sources["youtube_channels"].append(
                action["value"]
            )

        elif action["type"] == "delete_yt":

            sources["youtube_channels"].remove(
                action["value"]
            )

        elif action["type"] == "add_kw":

            filters["important_words"].append(
                action["value"]
            )

        elif action["type"] == "delete_kw":

            filters["important_words"].remove(
                action["value"]
            )

        save_json(
            SOURCES_FILE,
            sources
        )

        save_json(
            FILTERS_FILE,
            filters
        )

        st.session_state.pending_action = None

        st.sidebar.success(
            "Operazione completata!"
        )

        st.rerun()

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
