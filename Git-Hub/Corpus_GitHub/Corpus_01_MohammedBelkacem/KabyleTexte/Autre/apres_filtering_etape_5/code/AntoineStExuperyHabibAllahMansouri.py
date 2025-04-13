#!/usr/bin/env python3
import re
import sys

def process_file(input_file, output_file):
    # Lecture de l'ensemble du contenu du fichier Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
   
    # 1. Remplacer tous les retours à la ligne par un espace pour combler les coupures intempestives
    content = re.sub(r'\s*\n\s*', ' ', content)
    
    # 2. Réintroduire un saut de ligne lorsque l'on rencontre un signe de ponctuation indiquant la fin d'une phrase
    #    suivi d'un espace et d'une majuscule (on considère le point '.' et l'ellipses '…' comme marqueurs)
    content = re.sub(r'([\.…])\s+(?=[A-Z])', r'\1\n', content)
    
    # 3. Insertion d'un saut de ligne avant le tiret lorsque celui-ci suit un deux-points et des espaces.
    # Par exemple, "kan: - Ah! ..." deviendra "kan:\n- Ah! ..."
    content = re.sub(r'(?<=\S)\s+-\s+', '\n- ', content)
    
    content = re.sub(r'(?<=\S)\s+.\s+', '\n- ', content)
    # Nettoyage final : suppression d'espaces superflus en début et fin de texte
    content = content.strip()

    # Écriture du contenu traité dans le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    input_file = "../flexions_verbales.md"
    output_file = "flexions_verbales_corrige.md"
    process_file(input_file, output_file)
