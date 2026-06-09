import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_alert(alert):

    prompt = f"""
Sei un consulente editoriale per un canale YouTube
che parla di calcio, FIGC, Juventus, Inter,
arbitri, procure federali e giustizia sportiva.

IMPORTANTE:

Non inventare informazioni.

Usa esclusivamente i dati presenti
nel titolo e nella descrizione.

Se una informazione non è presente
nel titolo o nella descrizione:

NON dedurla.

NON ipotizzarla.

Scrivi:
"Non specificato nell'articolo."

Distingui chiaramente:
- fatti riportati
- ipotesi
- possibili conseguenze

TITOLO:
{alert['titolo']}

DESCRIZIONE:
{alert.get('description', '')}

FONTE:
{alert['fonte']}

LINK:
{alert['link']}

Rispondi in questo formato:

RIASSUNTO
Spiega la notizia in modo chiaro.

CONTESTO
Perché è importante.
Quali potrebbero essere le conseguenze.
Quali aspetti meritano attenzione.

IDEE CONTENUTO
- Idee video
- Domande per la community
- Possibili collegamenti ad altre notizie
- Titoli YouTube

PRIORITA
Numero da 1 a 10.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text