import os
import logging
import nltk
from transformers import pipeline
import torch

# Télécharger les ressources NLTK pour la segmentation en phrases
nltk.download('punkt')
nltk.download('punkt_tab')

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

# Seuil de confiance pour considérer une phrase comme française
CONFIDENCE_THRESHOLD = 0.7

def process_text(text, threshold=CONFIDENCE_THRESHOLD, batch_size=8):
    """
    Découpe le texte en phrases, traite les phrases par lots via le pipeline
    en activant le truncation pour éviter des séquences trop longues, puis regroupe
    les phrases françaises consécutives dans une balise <french>...</french>.
    """
    sentences = nltk.sent_tokenize(text)
    processed_sentences = []
    french_block = []
    results = []

    # Traitement par lots pour maximiser l'efficacité sur GPU
    for i in range(0, len(sentences), batch_size):
        batch_sentences = sentences[i:i+batch_size]
        # Utiliser truncation=True pour éviter les séquences trop longues
        batch_results = lang_detector(batch_sentences, truncation=True)
        results.extend(batch_results)

    # Itérer sur les phrases et leurs résultats respectifs
    for sentence, result in zip(sentences, results):
        lang = result['label'].replace('__label__', '') if 'label' in result else None
        score = result['score'] if 'score' in result else 0.0
        if score >= threshold and lang == 'fr':
            french_block.append(sentence)
        else:
            if french_block:
                processed_sentences.append("<french>" + " ".join(french_block) + "</french>")
                french_block = []
            processed_sentences.append(sentence)
    if french_block:
        processed_sentences.append("<french>" + " ".join(french_block) + "</french>")
    return "\n".join(processed_sentences)

def process_file(input_filepath, output_filepath):
    """
    Lit un fichier Markdown, applique le traitement du texte et sauvegarde le résultat.
    """
    logging.info(f"Traitement du fichier : {input_filepath}")
    with open(input_filepath, "r", encoding="utf-8") as infile:
        content = infile.read()
    processed_content = process_text(content)
    with open(output_filepath, "w", encoding="utf-8") as outfile:
        outfile.write(processed_content)
    logging.info(f"Fichier traité et sauvegardé dans : {output_filepath}")

def main():
    # Définir le répertoire source et le répertoire de sortie
    input_dir = "./Markdown_non/with_tables/"  # Adapté à votre chemin source
    output_dir = "./Markdown_tagged_roberta/with_tables"              # Répertoire de sortie
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
