import re
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
         logging.FileHandler("clean_text_log.log"),
         logging.StreamHandler()
    ]
)

def clean_text(text):
    """
    Nettoie une chaîne de caractères en :
      - Supprimant les espaces autour des tirets (pour transformer "i - d - yeţţilin" en "i-d-yeţţilin")
      - Remplaçant toute séquence d'espaces multiples par un seul espace
      - Supprimant les espaces en début et fin de chaîne
    """
    # Supprimer les espaces autour des tirets
    text = re.sub(r'\s*-\s*', '-', text)
    # Remplacer les espaces multiples par un seul espace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_file(input_filepath, output_filepath):
    """
    Parcourt le fichier Markdown en entrée, nettoie chaque ligne et sauvegarde le résultat dans un nouveau fichier Markdown.
    """
    logging.info(f"Lecture du fichier : {input_filepath}")
    try:
        with open(input_filepath, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier {input_filepath}: {e}")
        return

    logging.info(f"Nombre total de lignes lues : {len(lines)}")
    cleaned_lines = []
    for idx, line in enumerate(lines, start=1):
        cleaned_line = clean_text(line)
        cleaned_lines.append(cleaned_line + "\n")
        if idx % 1000 == 0:
            logging.info(f"{idx} lignes traitées...")

    logging.info(f"Écriture du fichier nettoyé : {output_filepath}")
    try:
        with open(output_filepath, "w", encoding="utf-8") as outfile:
            outfile.writelines(cleaned_lines)
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture du fichier {output_filepath}: {e}")
        return

    logging.info("Traitement complet du fichier.")

if __name__ == "__main__":
    # Spécifiez le fichier Markdown en entrée et le fichier de sortie
    input_filepath = "003-Omar Dahmoune.pdf.md_out.md"    # Par exemple, votre fichier à nettoyer
    output_filepath = "kabyleSentens_Balise_clean.md"  # Fichier nettoyé en sortie
    process_file(input_filepath, output_filepath)
