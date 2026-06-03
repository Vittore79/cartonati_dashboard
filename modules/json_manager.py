from modules.supabase_client import (
    add_alert
)

def save_alert(alert_data):

    with open(
        "debug_alert.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            str(alert_data) + "\n"
        )

    add_alert(alert_data)