def add_period_on_consecutive_uppercase_lines(input_path, output_path):
    # Lecture du fichier en supprimant les retours à la ligne
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.read().splitlines()

    updated_lines = []
    for i in range(len(lines) - 1):
        current_line = lines[i].strip()
        next_line = lines[i + 1].strip()
        
        # Vérifier que les deux lignes ne sont pas vides et commencent par une majuscule
        if current_line and next_line and current_line[0].isupper() and next_line[0].isupper():
            # Ajouter un point si la ligne ne se termine pas déjà par un point
            if not current_line.endswith('.'):
                current_line += '.'
        
        updated_lines.append(current_line)
    
    # Ajouter la dernière ligne (sans traitement)
    if lines:
        updated_lines.append(lines[-1].strip())
    
    # Écriture du résultat dans le fichier de sortie
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in updated_lines:
            outfile.write(line + '\n')

# Exemple d'utilisation :
add_period_on_consecutive_uppercase_lines('output.md','output2.md')
