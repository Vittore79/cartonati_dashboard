from modules.supabase_client import (
    get_rss_feeds,
    get_youtube_channels,
    get_keywords
)

def load_sources():

    rss_feeds = [
        row["url"]
        for row in get_rss_feeds()
    ]

    youtube_channels = []

    for row in get_youtube_channels():

        youtube_channels.append(
            {
                "name": row["name"],
                "id": row.get(
                    "channel_id",
                    ""
                )
            }
        )

    return {
        "rss_feeds": rss_feeds,
        "youtube_channels": youtube_channels
    }


def load_filters():

    keywords = [

        row["keyword"]

        for row in get_keywords()
    ]

    return {
        "important_words": keywords,
        "team_words": keywords,
        "youtube_words": keywords
    }