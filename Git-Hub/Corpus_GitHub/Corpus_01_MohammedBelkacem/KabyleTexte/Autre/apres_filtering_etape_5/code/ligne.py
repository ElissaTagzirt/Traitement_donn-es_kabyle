#!/usr/bin/env python3
import sys

def process_file(input_file, output_file):
    # Lecture du contenu complet du fichier
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Suppression de toutes les occurrences du caractère "ù"
    content = content.replace("ù", "")

    #Suppression de toutes les occurrences du caratére "-"
    content = content.replace("-", "")    
    # Écriture du contenu modifié dans le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    input_file = "corrige3.md"
    output_file = "corrige2.md"
    process_file(input_file, output_file)
