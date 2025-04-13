import re
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
         logging.FileHandler("merge_special_cases_log.log"),
         logging.StreamHandler()
    ]
)

def merge_special_cases(text):
    """
    Applique les remplacements suivants sur le texte :
      - "γa s" (avec espace(s)) devient "γas"
      - "n eγ" (avec espace(s)) devient "neγ"
      - "ğ ğ an" (avec espace(s)) devient "ğğan"
    """
    # Remplacer "γa s" par "γas"
    text = re.sub(r'γa\s+s', 'γas', text)
    # Remplacer "n eγ" par "neγ"
    text = re.sub(r'n\s+eγ', 'neγ', text)
    # Remplacer "ğ ğ an" par "ğğan"
    text = re.sub(r'ğ\s+ğ\s+an', 'ğğan', text)
    text = re.sub(r'ğ\s+ğ\s+en', 'ğğan', text)

    return text

def process_file(input_filepath, output_filepath):
    """
    Lit le fichier Markdown en entrée, applique les remplacements sur chaque ligne,
    et écrit le résultat dans un nouveau fichier Markdown.
    """
    logging.info(f"Lecture du fichier : {input_filepath}")
    try:
        with open(input_filepath, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier {input_filepath}: {e}")
        return

    processed_lines = []
    for idx, line in enumerate(lines, start=1):
        new_line = merge_special_cases(line)
        processed_lines.append(new_line)
        if idx % 1000 == 0:
            logging.info(f"{idx} lignes traitées...")

    try:
        with open(output_filepath, "w", encoding="utf-8") as outfile:
            outfile.writelines(processed_lines)
        logging.info(f"Fichier traité et sauvegardé dans : {output_filepath}")
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture du fichier {output_filepath}: {e}")

if __name__ == "__main__":

    input_filepath = "003-Omar Dahmoune.pdf.md_out.md"    # Nom du fichier Markdown en entrée
    output_filepath = "output_file.md"  # Nom du fichier Markdown en sortie
    process_file(input_filepath, output_filepath)
