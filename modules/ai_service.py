from modules.supabase_client import (
    get_alert_by_id,
    get_ai_analysis,
    save_ai_analysis
)

from modules.ai_analyzer import analyze_alert


def analyze_and_save(alert_id):

    existing = get_ai_analysis(alert_id)

    if existing:
        return existing

    alert = get_alert_by_id(alert_id)

    if not alert:
        return None

    result = analyze_alert(alert)

    save_ai_analysis(
        alert_id=alert_id,
        summary=result,
        context="",
        content_ideas="",
        priority=""
    )

    return get_ai_analysis(alert_id)