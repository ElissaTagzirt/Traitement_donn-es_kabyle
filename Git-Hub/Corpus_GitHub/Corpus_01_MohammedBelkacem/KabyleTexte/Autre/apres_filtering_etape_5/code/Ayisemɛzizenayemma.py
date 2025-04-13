#!/usr/bin/env python3
import re
import sys

def process_file(input_file, output_file):
    # Lecture de l'ensemble du contenu du fichier Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Supprimer tous les chiffres
    content = re.sub(r'\d+', '', content)
    
    # 2. Remplacer tous les retours à la ligne par un espace pour combler les coupures intempestives
    content = re.sub(r'\s*\n\s*', ' ', content)
    
    # 3. Réintroduire un saut de ligne lorsque l'on rencontre un signe de ponctuation indiquant la fin d'une phrase
    #    suivi d'un espace et d'une majuscule (c'est-à-dire le début d'une nouvelle phrase)
    #    Ici, on considère le point ('.') et l'ellipses ('…') comme marqueurs.
    content = re.sub(r'([\.…])\s+(?=[A-Z])', r'\1\n', content)
    
    # Suppression de toutes les occurrences du caractère "ù"
    content = content.replace("ù", "")

    # Optionnel : nettoyer d’éventuels espaces superflus en début/fin
    content = content.strip()
    
    # Écriture du contenu traité dans le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':

    input_file = "../Ditmurtnuɛekki.pdf.md"
    output_file = "Ditmurtnuɛekki.pdf_corrige.md"
    process_file(input_file, output_file)
