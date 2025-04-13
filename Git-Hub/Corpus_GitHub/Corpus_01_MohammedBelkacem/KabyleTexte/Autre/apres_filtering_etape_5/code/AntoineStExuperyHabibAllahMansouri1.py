#!/usr/bin/env python3
import sys

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_lines = []
    for line in lines:
        # Vérifier si la ligne contient un deux-points
        if ':' in line:
            # On sépare la ligne en deux parties : avant et après le premier deux-points
            term, separator, definition = line.partition(':')
            # Remplacer dans la partie définition les caractères indiqués
            definition = definition.replace('ḍ', 'v').replace('ǧ', 'o').replace('ẓ', 'é').replace('ṛ', 'ô').replace('tt', 'p').replace('ɣ', 'p')
            # Reconstituer la ligne avec le séparateur ':' entre les deux parties
            line = term + separator + definition
        processed_lines.append(line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

if __name__ == '__main__':
    input_file = "corrige3.md"
    output_file = "traduit.md"
    process_file(input_file, output_file)
