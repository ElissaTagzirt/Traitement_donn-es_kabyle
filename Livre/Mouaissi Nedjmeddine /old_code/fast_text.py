import os
import logging
import nltk
import fasttext

# Télécharger les ressources NLTK pour la tokenisation
nltk.download('punkt')

# Configuration du logging pour afficher et enregistrer les messages
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
         logging.FileHandler("process_log_fasttext.log"),
         logging.StreamHandler()
    ]
)

# Charger le modèle FastText pour la détection de langue
# Assurez-vous que le fichier "lid.176.bin" est accessible
model = fasttext.load_model("lid.176.bin")
logging.info("Modèle FastText 'lid.176.bin' chargé avec succès.")

# Seuil de confiance pour considérer qu'une ligne ou un mot est en français
CONFIDENCE_THRESHOLD = 0.8

def predict_language(text):
    """
    Retourne le label et la probabilité pour un texte donné en utilisant fastText.
    Le label retourné sera sous la forme '__label__fr', qu'on nettoie ensuite.
    """
    labels, probabilities = model.predict(text)
    # On récupère le premier label et probabilité
    label = labels[0].replace('__label__', '')
    probability = probabilities[0]
    return label, probability

def process_line(line, threshold=CONFIDENCE_THRESHOLD):
    """
    Traite une ligne du fichier Markdown.
    
    - Si la ligne est une entête (commence par '#') ou est vide, on la retourne telle quelle.
    - Sinon, on effectue d'abord une détection globale sur la ligne.
      Si la langue détectée est le français avec une confiance suffisante,
      on encadre la ligne par une balise <fr>...</fr>.
    - Sinon, on procède à une détection mot par mot et on entoure chaque token de <fr> ou <unk> selon le résultat.
    """
    # Ignorer les entêtes et les lignes vides
    if line.lstrip().startswith("#") or not line.strip():
        return line

    # Détection globale sur la ligne
    overall_label, overall_prob = predict_language(line)
    if overall_label == 'fr' and overall_prob >= threshold:
        return f"<fr>{line}</fr>#<{overall_prob}>"
    else:
        # Passage à une détection mot par mot
        tokens = nltk.word_tokenize(line)
        processed_tokens = []
        for token in tokens:
            token_label, token_prob = predict_language(token)
            if token_label == 'fr' and token_prob >= threshold:
                processed_tokens.append(f"<fr>{token}</fr>#<{token_prob}>")
            else:
                processed_tokens.append(f"<unk>{token}</unk>#<{token_prob}>")
        # Reconstitution de la ligne (la gestion fine de la ponctuation peut être améliorée)
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
    output_dir = "./test_resultat"  # Répertoire de sortie  # Répertoire de sortie
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
