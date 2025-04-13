import os
import logging
import nltk
from transformers import pipeline
import torch

# Télécharger les ressources NLTK pour la segmentation en phrases et tokenisation
nltk.download('punkt')

# Configuration du logging pour afficher et enregistrer les messages
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
         logging.FileHandler("process_log.log"),
         logging.StreamHandler()
    ]
)

# Définir le dispositif : GPU si disponible, sinon CPU
device = 0 if torch.cuda.is_available() else -1
logging.info(f"Utilisation du GPU: {'Oui' if device == 0 else 'Non'}")

# Charger le pipeline de détection de langue avec le GPU et activer le truncation
lang_detector = pipeline(
    "text-classification",
    model="papluca/xlm-roberta-base-language-detection",
    device=device
)

# Seuil de confiance pour considérer qu'une ligne ou un mot est en français
CONFIDENCE_THRESHOLD = 0.5

def process_line(line, threshold=CONFIDENCE_THRESHOLD):
    """
    Traite une ligne du fichier Markdown.
   
    - Si la ligne est une entête (commence par '#'), on la retourne telle quelle.
    - Sinon, on effectue d'abord une détection globale sur la ligne.
      Si le score est supérieur ou égal au seuil et que la langue détectée est le français,
      on entoure la ligne par une balise <fr>...</fr>.
    - Si le score global est insuffisant ou si la ligne semble contenir des mots non-français,
      on procède à une détection mot par mot et on entoure chaque token de <fr> ou <unk> selon le résultat.
    """
    # Ignorer les entêtes et les lignes vides
    if line.lstrip().startswith("#") or not line.strip():
        return line

    # Détection globale sur la ligne
    overall_result = lang_detector(line, truncation=True)
    overall_label = overall_result[0].get('label', '').replace('__label__', '')
    overall_score = overall_result[0].get('score', 0.0)

    if overall_label == 'fr' and overall_score >= threshold:
        return f"<fr>{line}</fr><{overall_score}>"
    else:
        # Passage à une détection mot par mot
        tokens = nltk.word_tokenize(line)
        processed_tokens = []
        for token in tokens:
            token_result = lang_detector(token, truncation=True)
            token_label = token_result[0].get('label', '').replace('__label__', '')
            token_score = token_result[0].get('score', 0.0)
            if token_label == 'fr' and token_score >= threshold:
                processed_tokens.append(f"<fr>{token}</fr><{token_score}>")
                
            else:
                processed_tokens.append(f"<unk>{token}</unk><{token_score}>")
        # On rejoint les tokens par un espace (la reconstruction exacte de la ponctuation peut être améliorée)
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
    input_dir = "./Markdown_non/without_tables/test"  # Adapté à votre chemin source
    output_dir = "./Markdown_tagged_roberta2/without_tables/test"  # Répertoire de sortie
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