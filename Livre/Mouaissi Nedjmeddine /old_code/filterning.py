import re

def filter_file(input_path, output_path):
    """
    Parcourt le fichier .mnd spécifié et écrit dans le fichier de sortie
    toutes les lignes après avoir effectué les opérations suivantes :
      - Supprime la ligne si elle contient uniquement un chiffre (après suppression des espaces).
      - Supprime la ligne si elle contient le mot "HEADER" (insensible à la casse).
      - Supprime la ligne si elle contient le mot "Corpus" (insensible à la casse).
      - Supprime la ligne si elle correspond au motif p(chiffre) (ex: p(5)).
      - Supprime la ligne si elle est composée uniquement d'astérisques.
      - Remplace dans les lignes restantes le mot "Extrait" par "Tukkist".
    """
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    filtered_lines = []
    for line in lines:
        stripped_line = line.strip()
        # Supprimer la ligne si elle est vide (ou ne contient que des espaces).
        if not stripped_line:
            continue
        # Supprimer la ligne si elle contient uniquement un nombre.
        if re.fullmatch(r'\d+', stripped_line):
            continue
        if re.search(r'-\s*\d+\s*-', line, flags=re.IGNORECASE):
            continue
        if re.search(r'Introduction', line, flags=re.IGNORECASE):
            continue
        # Supprimer la ligne si elle contient le mot "HEADER" (insensible à la casse).
        if re.search(r'\bHEADER\b', line, flags=re.IGNORECASE):
            continue
        # Supprimer la ligne si elle contient le mot "Corpus" (insensible à la casse).
        if re.search(r'\bCorpus\b', line, flags=re.IGNORECASE):
            continue
        # Supprimer la ligne si elle est composée uniquement d'astérisques.
        if re.fullmatch(r'\s*\*+\s*', line):
            continue
        if re.search(r'\bp\.\d+\b', line, flags=re.IGNORECASE):
            continue

        if re.fullmatch(r"\s*<\s*footer\s*>.*?<\s*/\s*footer\s*>\s*", line, flags=re.IGNORECASE):
            continue
        if re.fullmatch(r'### HEADER', line):
            continue
        if re.fullmatch(r"\s*\d+\s+http\s*:\s*/\s*\S+.*", line, flags=re.IGNORECASE):
            continue
        if re.fullmatch(r"\bIntroduction\b", line, flags=re.IGNORECASE):
            continue
        if re.search(r'\b[\d]*\s*https?\s*:\s*//[^\s<>"]+|www\.[^\s<>"]+', line, flags=re.IGNORECASE):
            continue
        
        # On initialise new_line à partir de la ligne lue
        new_line = line

        # Remplacement du mot "Extrait" par "Tukkist".
        new_line = new_line.replace("Extrait", "Tukkist")
        # Remplacement du mot "mais" par "maca".
        new_line = new_line.replace("mais", "maca")
        # Remplacement de "$" entouré d'espaces par "ɣ"
        new_line = re.sub(r'\s*\$\s*', 'ɣ', new_line, flags=re.UNICODE)
        new_line = re.sub(r'l\s*\’\s*usine', 'luzin', new_line, flags=re.UNICODE)
        new_line = re.sub(r'ê', 'ḥ', new_line, flags=re.UNICODE)
        new_line = re.sub(r'ç', 'č', new_line, flags=re.UNICODE)
        new_line = re.sub(r'ç', 'č', new_line, flags=re.UNICODE)
        new_line = re.sub(r'î', 'ṭ', new_line, flags=re.UNICODE)
        new_line = re.sub(r'é', 'ẓ', new_line, flags=re.UNICODE)
        new_line = re.sub(r'v', 'ḍ', new_line, flags=re.UNICODE)
        new_line = re.sub(r'£', 'Ɣ', new_line, flags=re.UNICODE)
      # Remplacement de "La poésie" par "Tamedyazt n " (insensible à la casse)
        new_line = re.sub(r'La\s+poésie', "Tamedyazt n ", new_line, flags=re.IGNORECASE)
        # Remplacement de "interpréter par" par "Ttwasefser seɣur" (insensible à la casse)
        new_line = re.sub(r'interpréter\s+par', "Ttwasefser seɣur", new_line, flags=re.IGNORECASE)
        # Supprimer un motif de la forme "( pp . 22-23 )"
        new_line = re.sub(r'\(\s*pp\s*\.\s*\d+\s*-\s*\d+\s*\)', '', new_line, flags=re.IGNORECASE)
        # Supprimer le motif "( p. chiffre )"
        new_line = re.sub(r"\(\s*p\.\s*\d+\s*\)", "", new_line)
        # Supprimer le motif "( 11 )" suivi d'un espace
        new_line = re.sub(r'\(\s*\d+\s*\)\s', '', new_line)
        # Remplacer un motif de type "40 ." par "-"
        new_line = re.sub(r'\d+\s*\.\s*', '-', new_line)

        filtered_lines.append(new_line)
        
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(filtered_lines)

def main():
    input_file = "./Markdown_tagged_roberta2/without_tables/beaucoup_de_francais/clean/clean_630_Mas. Amz. 631.md"  # Chemin de ton fichier .mnd
    output_file = "./Markdown_tagged_roberta2/without_tables/beaucoup_de_francais/clean/clean_waggi_630.md"       # Chemin de sortie pour le fichier filtré
    filter_file(input_file, output_file)
    print(f"Traitement terminé. Le fichier filtré est enregistré dans : {output_file}")

if __name__ == '__main__':
    main()
