import json
import os

JSON_FILE = "alerts.json"

# =========================
# CREA FILE
# =========================

if not os.path.exists(JSON_FILE):

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump([], file)

# =========================
# SALVA ALERT
# =========================

def save_alert(alert_data):

    try:

        with open(
            JSON_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            alerts = json.load(file)

    except:

        alerts = []

    alerts.insert(0, alert_data)

    # massimo 500 alert
    alerts = alerts[:500]

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            alerts,
            file,
            ensure_ascii=False,
            indent=4
        )