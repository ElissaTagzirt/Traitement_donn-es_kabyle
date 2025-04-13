#!/usr/bin/env python3
import re
import sys

def flip_text(text):
    # Dictionnaire de conversion des caractères upside down vers leur équivalent normal
    mapping = {
        'ɐ': 'a',  'ʍ': 'w',  'z': 'z',  'ı': 'i',  'ʇ': 't',
        'q': 'b',  'ɔ': 'c',  'p': 'd',  'ǝ': 'e',  'ɟ': 'f',
        'ƃ': 'g',  'ɥ': 'h',  'ɾ': 'j',  'ʞ': 'k',  'ן': 'l',
        'ɯ': 'm',  'u': 'n',  'o': 'o',  'd': 'p',  'b': 'q',
        'ɹ': 'r',  's': 's',  'n': 'u',  'ʌ': 'v',  'x': 'x',
        'ʎ': 'y',
        'ɣ': 'g',
        '˙': '.',  # conversion du point inversé
        'Ɩ': 'i',  # conversion pour la majuscule I inversée
        'ᄅ': 'r',  # conversion du symbole inversé en r
        'Ɛ': 'ɛ'   # conversion pour ɛ inversé
    }
    # On parcourt la chaîne à l'envers et on remplace chaque caractère selon le mapping,
    # ou on garde le caractère s'il n'est pas dans le dictionnaire.
    return ''.join(mapping.get(char, char) for char in reversed(text))

def process_file(input_file, output_file):
    # Lecture de l'ensemble du contenu du fichier Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Transformation du texte upside down en texte normal
    content = flip_text(content)
    
    # 1. Supprimer tous les chiffres
    content = re.sub(r'\d+', '', content)
    
    # 2. Remplacer tous les retours à la ligne par un espace pour combler les coupures intempestives
    content = re.sub(r'\s*\n\s*', ' ', content)
    
    # 3. Réintroduire un saut de ligne lorsque l'on rencontre un signe de ponctuation indiquant la fin d'une phrase
    #    suivi d'un espace et d'une majuscule (on considère le point '.' et l'ellipses '…' comme marqueurs)
    content = re.sub(r'([\.…])\s+(?=[A-Z])', r'\1\n', content)
    
    # Nettoyage final : suppression d'espaces superflus en début et fin de texte
    content = content.strip()
    
    # Écriture du contenu traité dans le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    input_file = "../Alug n taneyt - Cahier de coloriage.md"
    output_file = "Alug n taneyt - Cahier de coloriage_corrige1.md"
    process_file(input_file, output_file)
