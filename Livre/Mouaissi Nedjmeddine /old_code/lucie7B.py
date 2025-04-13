import os
import logging
import nltk
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Télécharger les ressources NLTK pour la tokenisation
nltk.download('punkt')

# Configuration du logging pour afficher et enregistrer les messages
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
         logging.FileHandler("process_log_lucie.log"),
         logging.StreamHandler()
    ]
)

# Définir le dispositif : GPU si disponible, sinon CPU
device = 0 if torch.cuda.is_available() else -1
logging.info(f"Utilisation du GPU: {'Oui' if device == 0 else 'Non'}")

# Charger le modèle Lucie-7B pour la détection de langue via prompt
model_name = "OpenLLM-France/Lucie-7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
logging.info(f"Modèle '{model_name}' chargé avec succès.")

# Création du pipeline de génération (sans passer explicitement le device)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Seuil de confiance pour considérer qu'une ligne ou un mot est en français
CONFIDENCE_THRESHOLD = 0.8

def predict_language(text):
    """
    Retourne le label et une valeur de confiance simulée pour un texte donné en utilisant Lucie-7B via prompt.
    Le prompt demande d'indiquer uniquement la langue du texte fourni.
    """
    prompt = f"Indique uniquement la langue du texte suivant :\n\n{text}\n\nLangue:"
    print("Texte pour la détection :", text)
    print("Prompt envoyé :", prompt)
    outputs = generator(prompt, max_length=50, truncation=True, do_sample=False)
    generated_text = outputs[0]['generated_text']
    if "Langue:" in generated_text:
        # Extraction du premier mot après "Langue:"
        detected = generated_text.split("Langue:")[1].strip().split()[0].lower()
        # Valeur de confiance simulée : 1.0 si la langue est le français, sinon 0.5
        confidence = 1.0 if detected in ["fr", "français"] else 0.5
        return detected, confidence
    return "unknown", 0.0

def process_line(line, threshold=CONFIDENCE_THRESHOLD):
    """
    Traite une ligne du fichier Markdown.

    - Si la ligne est une entête (commence par '#') ou est vide, elle est retournée telle quelle.
    - Sinon, on effectue une détection globale sur la ligne.
      Si la langue détectée est le français avec une confiance suffisante,
      la ligne est encadrée par une balise <fr>...</fr> suivie de la probabilité.
    - Sinon, on procède à une détection mot par mot et on entoure chaque token de <fr> ou <unk>
      selon le résultat, en ajoutant également la valeur de confiance.
    """
    # Vérifier si la ligne est une entête ou vide
    print(line)
    if line.lstrip().startswith("#") or not line.strip():
        return line

    # Ici, la ligne est non vide et doit être traitée
    logging.info(f"Traitement de la ligne : {line}")
    
    # Détection globale sur la ligne
    overall_label, overall_prob = predict_language(line)
    if overall_label == 'fr' and overall_prob >= threshold:
        return f"<fr>{line}</fr>#<{overall_prob}>"
    else:
        # Passage à une détection mot par mot
        tokens = nltk.word_tokenize(line)
        processed_tokens = []
        for token in tokens:
            # Vérifier si le token n'est pas vide (normalement, nltk.word_tokenize ne renvoie pas de token vide)
            if token.strip():
                token_label, token_prob = predict_language(token)
                if token_label == 'fr' and token_prob >= threshold:
                    processed_tokens.append(f"<fr>{token}</fr>#<{token_prob}>")
                else:
                    processed_tokens.append(f"<unk>{token}</unk>#<{token_prob}>")
        return " ".join(processed_tokens)

def process_file(input_filepath, output_filepath):
    """
    Lit un fichier Markdown ligne par ligne, applique le traitement sur chaque ligne et sauvegarde le résultat.
    """
    logging.info(f"Traitement du fichier : {input_filepath}")
    with open(input_filepath, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
    processed_lines = [process_line(line.rstrip('\n')) for line in lines]

    with open(output_filepath, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(processed_lines))
    logging.info(f"Fichier traité et sauvegardé dans : {output_filepath}")

def main():
    # Définir le répertoire source et le répertoire de sortie
    input_dir = "./Markdown_non/without_tables/test"  # Chemin source adapté
    output_dir = "./test_resultat"  # Répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)

    # Liste des fichiers .md à traiter
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    logging.info(f"Nombre de fichiers à traiter : {len(md_files)}")

    # Traiter chaque fichier
    for md_file in md_files:
        input_filepath = os.path.join(input_dir, md_file)
        output_filepath = os.path.join(output_dir, md_file)
        process_file(input_filepath, output_filepath)

    logging.info("Traitement complet de tous les fichiers.")

if __name__ == "__main__":
    main()
