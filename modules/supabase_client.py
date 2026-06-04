from supabase import create_client
from datetime import datetime

SUPABASE_URL = "https://ptoavbkqgxdxqhyloezv.supabase.co"

SUPABASE_KEY = "sb_publishable__gilPXeZDfblncxvc7BHsQ_hyr6UkQ1"

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
            {
                "url": url
            }
        )
        .execute()
    )


def delete_rss_feed(url):

    (
        supabase
        .table("rss_feeds")
        .delete()
        .eq(
            "url",
            url
        )
        .execute()
    )

# =========================
# YOUTUBE CHANNELS
# =========================

def get_youtube_channels():

    response = (
        supabase
        .table("youtube_channels")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


def add_youtube_channel(
    name,
    link,
    channel_id=""
):

    (
        supabase
        .table("youtube_channels")
        .insert(
            {
                "name": name,
                "link": link,
                "channel_id": channel_id
            }
        )
        .execute()
    )


def delete_youtube_channel(link):

    (
        supabase
        .table("youtube_channels")
        .delete()
        .eq(
            "link",
            link
        )
        .execute()
    )
    
# =========================
# ALERTS
# =========================

def get_alerts():

    response = (
        supabase
        .table("alerts")
        .select("*")
        .order(
            "data",
            desc=True
        )
        .execute()
    )

    return response.data


def add_alert(alert_data):

    print("INVIO ALERT A SUPABASE")

    result = (
        supabase
        .table("alerts")
        .insert(
            {
                "tipo": alert_data["tipo"],
                "titolo": alert_data["titolo"],
                "fonte": alert_data["fonte"],
                "link": alert_data["link"],
                "data": alert_data.get(
                   "data",
                   ""
                )
            }
)
        .execute()
    )

    print(result)
    

def update_last_scan():

    supabase.table("settings").update(
        {
            "last_scan": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        }
    ).eq("id", 1).execute()


def get_last_scan():

    result = (
        supabase
        .table("settings")
        .select("last_scan")
        .eq("id", 1)
        .execute()
    )

    if result.data:
        return result.data[0]["last_scan"]

    return "Mai"