import os
from supabase import create_client
from datetime import datetime
from zoneinfo import ZoneInfo

SUPABASE_URL = "https://ptoavbkqgxdxqhyloezv.supabase.co"

# La chiave segreta va configurata nelle Secrets di Streamlit Cloud
# oppure come variabile d'ambiente SUPABASE_SECRET_KEY sul server che esegue main.py.
try:
    import streamlit as st
    SUPABASE_KEY = st.secrets.get("SUPABASE_SECRET_KEY")
except Exception:
    SUPABASE_KEY = None

if not SUPABASE_KEY:
    SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")

if not SUPABASE_KEY:
    raise RuntimeError(
        "Manca SUPABASE_SECRET_KEY: configurala nelle Secrets di Streamlit "
        "oppure nelle variabili d'ambiente del server."
    )

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================
# KEYWORDS
# =========================

def get_keywords():

    response = (
        supabase
        .table("keywords")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


def add_keyword(keyword):

    (
        supabase
        .table("keywords")
        .insert(
            {
                "keyword": keyword
            }
        )
        .execute()
    )


def delete_keyword(keyword):

    (
        supabase
        .table("keywords")
        .delete()
        .eq(
            "keyword",
            keyword
        )
        .execute()
    )

# =========================
# RSS FEEDS
# =========================

def get_rss_feeds():

    response = (
        supabase
        .table("rss_feeds")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


def add_rss_feed(url):

    (
        supabase
        .table("rss_feeds")
        .insert(
