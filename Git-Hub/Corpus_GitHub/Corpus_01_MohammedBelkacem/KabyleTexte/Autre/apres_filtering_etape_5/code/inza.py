def merge_lines_condition(input_path, output_path):
    # Lecture du fichier et récupération des lignes sans les retours à la ligne
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.read().splitlines()
    
    merged_lines = []
    i = 0
    # Parcours de toutes les lignes
    while i < len(lines):
        # On commence avec la ligne courante (en retirant les espaces inutiles)
        current_line = lines[i].strip()
        
        # Tant qu'il existe une ligne suivante et que la condition est vérifiée :
        # la ligne courante ne se termine pas par un point et la suivante ne commence pas par une majuscule
        while i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if current_line and not current_line.endswith('.') and next_line and not next_line[0].isupper():
                # Fusionner la ligne suivante à la ligne courante en ajoutant un espace
                current_line = current_line + " " + next_line
                i += 1  # on saute la ligne fusionnée
            else:
                break
        
        # Ajouter la ligne (fusionnée ou non) à la liste résultat
        merged_lines.append(current_line)
        i += 1  # passer à la ligne suivante

    # Écriture des lignes fusionnées dans le fichier de sortie
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in merged_lines:
            outfile.write(line + '\n')

# Exemple d'utilisation
merge_lines_condition('output.md', 'output2.md')
