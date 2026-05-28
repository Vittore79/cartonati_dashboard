import requests

BOT_TOKEN = "8312714597:AAGXOyaW8b1k_PBS0OYf92MdgoDP2fImJXs"
CHAT_ID = "7494998558"

def send_message(text):

```
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": text
}

try:

    requests.post(
        url,
        json=payload,
        timeout=10
    )

    print("Messaggio Telegram inviato")

except Exception as error:

    print("Errore Telegram:", error)
```

