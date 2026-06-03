from modules.supabase_client import get_keywords

try:

    data = get_keywords()

    print("CONNESSIONE OK")
    print(data)

except Exception as error:

    print("ERRORE")
    print(error)