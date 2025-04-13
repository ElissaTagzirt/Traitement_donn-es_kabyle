import os
import logging
import nltk
from transformers import pipeline
import torch

# Télécharger les ressources NLTK pour la tokenisation
import nltk
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

# Seuil de confiance pour considérer qu'une ligne ou un mot est en français
CONFIDENCE_THRESHOLD = 0.5

def process_file(input_filepath, output_filepath):
    """
    Lit un fichier Markdown ligne par ligne, traite les lignes non entêtes en batch
    pour la détection globale, puis traite individuellement celles qui ne passent pas le test
    global en détection token par token. Le résultat est sauvegardé dans output_filepath.
    """
    logging.info(f"Traitement du fichier : {input_filepath}")
    with open(input_filepath, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    # Indices et contenu des lignes à traiter (non entêtes et non vides)
    indices_to_process = []
    non_header_lines = []
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#") or not line.strip():
            continue
        indices_to_process.append(i)
        non_header_lines.append(line.strip())

    # Traitement en batch des lignes sélectionnées
    if non_header_lines:
        batch_results = lang_detector(non_header_lines, truncation=True)
    else:
        batch_results = []

    # Préparer la liste des lignes traitées
    processed_lines = lines.copy()

    # Pour chaque ligne traitée en batch, appliquer la logique de détection
    for idx, result in zip(indices_to_process, batch_results):
        label = result.get('label', '').replace('__label__', '')
        score = result.get('score', 0.0)
        # Si la ligne est globalement considérée comme française
        if label == 'fr' and score >= CONFIDENCE_THRESHOLD:
            processed_lines[idx] = f"<fr>{lines[idx].strip()}</fr>\n"
        else:
            # Passage à une détection mot par mot
            tokens = nltk.word_tokenize(lines[idx])
            processed_tokens = []
            for token in tokens:
                token_result = lang_detector(token, truncation=True)[0]
                token_label = token_result.get('label', '').replace('__label__', '')
                token_score = token_result.get('score', 0.0)
                if token_label == 'fr' and token_score >= CONFIDENCE_THRESHOLD:
                    processed_tokens.append(f"<fr>{token}</fr>")
            processed_lines[idx] = " ".join(processed_tokens) + "\n"

    with open(output_filepath, "w", encoding="utf-8") as outfile:
        outfile.write("".join(processed_lines))
    logging.info(f"Fichier traité et sauvegardé dans : {output_filepath}")

def main():
    # Définir le répertoire source et le répertoire de sortie
    input_dir = "../data/pdfs_etat_2_separation/lot1/a_revoir"  # Chemin source adapté
    output_dir = "../data/pdfs_etat_3_tagged/lot1/a_revoir"  # Répertoire de sortie
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
