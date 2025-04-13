import re

def process_file(input_path, output_path):
    # Lecture du fichier d'entrée et suppression des espaces superflus et des lignes vides
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
    # On retire les espaces en début/fin de ligne et on élimine les lignes vides
    lines = [line.strip() for line in raw_lines if line.strip() != '']

    # Vérification sur les lignes consécutives :
    # Si une ligne commence par une majuscule ET que la ligne suivante commence aussi par une majuscule,
    # alors on s'assure que la ligne actuelle se termine par un point.
    for i in range(len(lines) - 1):
        current_line = lines[i]
        next_line = lines[i+1]
        if current_line and current_line[0].isupper() and next_line and next_line[0].isupper():
            if not current_line.endswith('.'):
                lines[i] = current_line + '.'

    # Regrouper tout le texte en un seul bloc en utilisant un espace comme séparateur
    text_block = " ".join(lines)

    # Utiliser une expression régulière pour ajouter un saut de ligne après un point
    # lorsque le mot qui suit (après l'espace) commence par une majuscule.
    modified_text = re.sub(r'\.\s+(?=[A-Z])', '.\n', text_block)

    # Écriture du texte modifié dans le fichier de sortie
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified_text)

# Exemple d'utilisation:
process_file('../Ditmurtnuɛekki.pdf.md', 'Ditmurtnuɛekki.pdf_corrige.md')
