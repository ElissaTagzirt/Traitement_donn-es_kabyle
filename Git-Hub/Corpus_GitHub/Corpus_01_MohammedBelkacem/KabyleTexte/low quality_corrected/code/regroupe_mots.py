import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
         logging.FileHandler("grouping_log.log"),
         logging.StreamHandler()
    ]
)

def process_lines(lines):
    """
    Parcourt la liste de lignes et regroupe avec la ligne précédente
    si la ligne courante contient moins de 4 mots.
    """
    output_lines = []
    for idx, line in enumerate(lines, start=1):
        # Nettoyer la ligne (enlever espaces superflus et retours à la ligne)
        cleaned_line = line.strip()
        if not cleaned_line:
            continue  # ignorer les lignes vides

        # Compter les mots
        words = cleaned_line.split()
        num_words = len(words)
        logging.info(f"Ligne {idx}: {num_words} mot(s) -> {cleaned_line}")

        if num_words < 4 and output_lines:
            # Regrouper avec la ligne précédente
            output_lines[-1] += " " + cleaned_line
            logging.info(f"  -> Regroupée avec la ligne précédente.")
        else:
            # Conserver la ligne telle quelle
            output_lines.append(cleaned_line)
            logging.info(f"  -> Nouvelle ligne ajoutée.")

    return output_lines

def process_file(input_filepath, output_filepath):
    """
    Lit le fichier Markdown en entrée, traite le regroupement des lignes,
    puis sauvegarde le résultat dans un nouveau fichier Markdown.
    """
    try:
        with open(input_filepath, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
        logging.info(f"Lecture du fichier {input_filepath} réussie ({len(lines)} lignes).")
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier {input_filepath}: {e}")
        return

    # Traitement des lignes
    grouped_lines = process_lines(lines)
    logging.info(f"Nombre de lignes après regroupement : {len(grouped_lines)}")

    # Écriture du fichier de sortie
    try:
        with open(output_filepath, "w", encoding="utf-8") as outfile:
            # On ajoute un retour à la ligne après chaque ligne
            for line in grouped_lines:
                outfile.write(line + "\n")
        logging.info(f"Fichier traité et sauvegardé dans : {output_filepath}")
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture du fichier {output_filepath}: {e}")

if __name__ == "__main__":
    input_filepath = "003-Omar Dahmoune.pdf.md_out.md"        # Remplacer par le nom de votre fichier d'entrée
    output_filepath = "mdhdhdh.md"     # Nom du fichier de sortie
    process_file(input_filepath, output_filepath)
