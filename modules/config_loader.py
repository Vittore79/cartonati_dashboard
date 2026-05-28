import json

# =========================
# CARICA SOURCES
# =========================

def load_sources():

    with open(
        "config/sources.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)

# =========================
# CARICA FILTERS
# =========================

def load_filters():

    with open(
        "config/filters.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)