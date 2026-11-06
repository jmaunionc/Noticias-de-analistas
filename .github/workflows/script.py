import os
import datetime
from google import genai
from google.genai import types

ANALISTAS = [
    "Michael Burry",
    "Bill Ackman",
    "Stanley Druckenmiller",
    "David Tepper",
    "Michael Hartnett",
    "Ed Yardeni",
    "Marko Kolanovic",
    "Mike Wilson",
    "Ray Dalio",
    "Warren Buffett",
    "Seth Klarman",
    "Howard Marks",
    "Terry Smith",
    "Jeremy Grantham",
    "Charlie Munger",
    "Geraldine Weiss"
]

HOY = datetime.date.today().strftime("%Y-%m-%d")

# Inicializa el cliente usando la API Key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def escanear_analista(nombre):
    prompt = f"""
    Realiza una búsqueda web exhaustiva sobre las opiniones, análisis, entrevistas, cartas a inversores o movimientos de cartera (13F) recientes de '{nombre}' en las últimas semanas ({HOY}).
    
    Busca específicamente:
    1. Declaraciones recientes sobre la situación macroeconómica o mercado global.
    2. Publicaciones de cartas a inversores, entrevistas destacadas o notas de investigación.
    3. Cambios conocidos en sus posiciones de cartera o tesis de inversión.

    Genera un informe ejecutivo conciso en español.
    Si no hay novedades relevantes o declaraciones recientes en el último mes, responde únicamente: "Sin novedades recientes".
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}]
            )
        )
        return response.text
    except Exception as e:
        return f"Error al consultar {nombre}: {str(e)}"

if __name__ == "__main__":
    informe_acumulado = f"=== INFORME DIARIO DE ANALISTAS Y GESTORES - {HOY} ===\n\n"
    
    for persona in ANALISTAS:
        print(f"Procesando: {persona}...")
        resumen = escanear_analista(persona)
        print(resumen)
        informe_acumulado += f"### {persona}\n{resumen}\n\n" + "="*40 + "\n\n"

    # Guardar el informe acumulado en un archivo de texto local
    nombre_archivo = f"informe_analistas_{HOY}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(informe_acumulado)
    print(f"Informe guardado correctamente en {nombre_archivo}")
