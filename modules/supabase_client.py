        .eq("id", alert_id)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None


def ai_analysis_exists(alert_id):

    result = (
        supabase
        .table("ai_analysis")
        .select("id")
        .eq("alert_id", alert_id)
        .execute()
    )

    return len(result.data) > 0

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
                "description": alert_data.get(
                    "description",
                    ""
                ),
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
            "last_scan": datetime.now(
                ZoneInfo("Europe/Rome")
            ).strftime(
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
    
    # =========================
# AI ANALYSIS
# =========================

def get_ai_analysis(alert_id):

    result = (
        supabase
        .table("ai_analysis")
        .select("*")
        .eq("alert_id", alert_id)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None


def save_ai_analysis(
    alert_id,
    summary,
    context,
    content_ideas,
    priority
):

    (
        supabase
        .table("ai_analysis")
        .insert(
            {
                "alert_id": alert_id,
                "summary": summary,
                "context": context,
                "content_ideas": content_ideas,
                "priority": priority
            }
        )
        .execute()
    )
