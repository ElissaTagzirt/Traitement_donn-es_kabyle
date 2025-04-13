import os
import time
from openai import OpenAI

# Tentative d'importation de RateLimitError ; sinon, utilisation d'une exception générique
try:
    from openai.error import RateLimitError
except ModuleNotFoundError:
    print("Le module openai.error n'est pas disponible, utilisation d'une exception générique pour RateLimitError.")
    RateLimitError = Exception  # Remplace par une exception plus générique

api_key = os.getenv("_")
client = OpenAI(api_key=api_key)


def remove_french_words(text):
    prompt = (
        "Veuillez supprimer tous les mots qui sont en français dans le texte suivant "
        "et renvoyer uniquement le texte contenant les mots kabyle. "
        "Tu me nettoies ce fichier pour être utilisé pour l'entraînement d'un modèle. "
        "Conservez la structure et la ponctuation du texte autant que possible.\n\n"
        "Texte d'origine :\n" + text
    )
    max_retries = 5
    delay = 10
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un assistant spécialisé dans le traitement de texte qui supprime les mots français d'un texte, en ne conservant que les mots dans d'autres langues."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            print(f"Erreur de taux atteint, tentative {attempt + 1} sur {max_retries}. Attente de {delay} secondes.")
            time.sleep(delay)
    raise Exception("Le quota de requêtes a été dépassé après plusieurs tentatives.")

if __name__ == "__main__":
    input_filename = "recttescuisine.md"
    output_filename = "recttescuisine_cleaned.md"
    
    with open(input_filename, "r", encoding="utf-8") as infile:
        original_text = infile.read()
    
    cleaned_text = remove_french_words(original_text)
    
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write(cleaned_text)
    
    print(f"Le fichier nettoyé a été sauvegardé sous le nom '{output_filename}'.")