import os
import re
from langdetect import detect, DetectorFactory

# Pour assurer la reproductibilité des détections de langue
DetectorFactory.seed = 0

def fusionner_mots_coupes(lines):
    """
    Fusionne les mots coupés par un tiret en fin de ligne avec le début de la ligne suivante.
    Par exemple, "ass-" en fin de ligne et "nni" en début de ligne deviennent "ass-nni".
    """
    i = 0
    while i < len(lines) - 1:
        # Si la ligne se termine par un tiret suivi d'espaces éventuels
        if re.search(r'-\s*$', lines[i]):
            # On retire le tiret final et on fusionne avec la ligne suivante (après suppression des espaces en début de ligne)
            lines[i] = re.sub(r'-\s*$', '', lines[i])
            lines[i] = lines[i] + '-' + lines[i+1].lstrip()
            # Supprime la ligne suivante, désormais fusionnée
            lines.pop(i+1)
            continue  # Réévalue la ligne i, au cas où il y aurait une suite de coupures
        i += 1
    return lines

def supprimer_bruits_typographiques(lines):
    """
    Supprime les lignes correspondant à des bruits typographiques,
    par exemple les lignes composées uniquement du motif "Sb. 03" (avec ou sans espaces).
    Gère aussi le cas où "Sb." et le numéro apparaissent sur deux lignes consécutives.
    """
    resultat = []
    i = 0
    # Motif pour une ligne entière du type "Sb. 03", insensible à la casse et autorisant des espaces
    motif_sb = re.compile(r'^\s*[Ss][Bb]\.\s*\d+\s*$')
    while i < len(lines):
        line = lines[i]
        if motif_sb.match(line):
            i += 1
            continue
        # Cas où "Sb." seul est sur une ligne et le numéro sur la suivante
        if re.match(r'^\s*[Ss][Bb]\.\s*$', line) and i + 1 < len(lines) and re.match(r'^\s*\d+\s*$', lines[i+1]):
            i += 2
            continue
        resultat.append(line)
        i += 1
    return resultat

def extraire_traductions(lines):
    """
    Extrait les lignes de traduction de type "mot : mot" lorsque la partie après le deux-points
    est détectée comme étant en français.
    
    Retourne deux listes :
      - traductions : contenant les traductions sous la forme "mot_kabyle : mot_francais"
      - lignes_sans_trads : les lignes restantes sans les traductions.
    """
    traductions = []
    lignes_sans_trads = []
    for line in lines:
        if ':' in line:
            partie_gauche, partie_droite = line.split(':', 1)
            mot_kabyle = partie_gauche.strip()
            mot_francais = partie_droite.strip()
            if mot_kabyle and mot_francais:
                try:
                    langue = detect(mot_francais)
                except Exception:
                    langue = None
                if langue == 'fr':
                    traductions.append(f"{mot_kabyle} : {mot_francais}")
                    continue  # Ne pas inclure cette ligne dans le texte principal
        lignes_sans_trads.append(line)
    return traductions, lignes_sans_trads

def fusionner_lignes_courtes(lines):
    """
    Fusionne les lignes courtes (1 ou 2 mots) selon les règles suivantes :
      - Si une ligne courte suit une ligne qui NE se termine PAS par un point final, 
        elle est fusionnée avec la ligne précédente.
      - Si la ligne précédente SE termine par un point, 
        la ligne courte est fusionnée avec la ligne précédente de cette dernière (si elle existe).
    """
    resultat = []
    for line in lines:
        mots = line.strip().split()
        if 1 <= len(mots) <= 2:  # Ligne courte
            if not resultat:
                # S'il n'y a aucune ligne précédente, on ajoute telle quelle
                resultat.append(line.strip())
            else:
                derniere = resultat[-1]
                if derniere.endswith('.'):
                    # La dernière ligne se termine par un point
                    if len(resultat) >= 2:
                        # Fusionne la ligne courte avec la ligne encore au-dessus
                        resultat[-2] = resultat[-2].rstrip() + ' ' + line.strip()
                    else:
                        resultat.append(line.strip())
                else:
                    # Sinon, fusionne avec la dernière ligne
                    resultat[-1] = derniere.rstrip() + ' ' + line.strip()
        else:
            resultat.append(line.strip())
    return resultat

def clean_kabyle_text_with_merge(text):
    """
    Nettoie et restructure un texte kabyle brut.
    
    Étapes appliquées :
      1. Nettoyage de base : suppression d'emails, URLs.
      2. Découpage en lignes et filtrage des lignes indésirables (pages, en-têtes, signatures, etc.).
      3. Nettoyage intraligne : suppression des contenus inutiles (parenthèses, nombres formatés, etc.).
      4. Fusion des mots coupés par un tiret sur plusieurs lignes.
      5. Suppression des bruits typographiques (ex. "Sb. 03").
      6. Extraction des traductions kabyle-français (lignes "mot : mot" détectées comme traduction).
      7. Fusion intelligente des lignes courtes (1 ou 2 mots) selon le contexte (selon la ponctuation de la ligne précédente).
      8. Réinsertion des traductions sous l'en-tête "# traduction" à la fin du texte.
    """
    # Étape 1 : Nettoyage de base (emails, URLs)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'http[s]?://\S+|www\.\S+', ' ', text)
    
    # Étape 2 : Découpage en lignes et filtrage
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Filtrage des lignes indésirables :
        # - Lignes composées uniquement de chiffres (pages, années isolées)
        if re.fullmatch(r'\d+', stripped):
            continue
        # - En-têtes du magazine ("Tiɣremt - Un ..." ou "Tiɣremt - Sem ...")
        if re.match(r'^Tiɣremt\s*-\s*(?:Un|Sem)\s+\d+', stripped):
            continue
        # - Lignes contenant des mots-clés non pertinents (email, téléphone, etc.)
        if any(word in stripped for word in ["E-mail", "Asmel", "tilifun"]):
            continue
        if '@' in stripped or 'www.' in stripped:
            continue
        if stripped.startswith("Aɣaram"):
            continue
        if "yimḍebbren n uɣmis" in stripped:
            continue
        # - Lignes avec plusieurs deux-points et chiffres
        if stripped.count(':') > 1 and re.search(r'\d', stripped):
            continue
        # - Lignes entièrement en majuscules (titres ou signatures isolées)
        letters_only = ''.join(ch for ch in stripped if ch.isalpha())
        if letters_only and letters_only.isupper():
            continue
        # - Lignes de type "Label : NomPropre" (souvent signatures ou références)
        if ':' in stripped:
            before, after = stripped.split(':', 1)
            parts = re.split(r'[\/,]\s*', after.strip())
            if all(part and part.split()[0][0].isupper() for part in parts):
                continue
        # - Lignes de simples initiales ou codes (ex: "T.O.A." ou "Sb.06")
        if re.fullmatch(r'(?:[A-Z]\.){2,}', stripped) or re.fullmatch(r'[A-Za-z]{1,3}\.\s*\d+', stripped):
            continue

        # Nettoyage intraligne :
        # Supprime le contenu entre parenthèses s'il contient un nombre ou seulement des noms isolés
        line_text = re.sub(r'\(([^)]+)\)', 
                           lambda m: "" if re.search(r'\d', m.group(1)) or 
                                        all(w and w[0].isupper() for w in m.group(1).split())
                           else m.group(0), 
                           stripped)
        # Supprime les nombres formatés (ex: 100.000,00)
        line_text = re.sub(r'\d{1,3}\.\d{3},\d{2}', ' ', line_text)
        # Supprime à nouveau les URLs/emails restants
        line_text = re.sub(r'http[s]?://\S+|www\.\S+|\S+@\S+', ' ', line_text)
        # Supprime les codes courts du type "Xx.00"
        line_text = re.sub(r'\b[A-Za-z]{1,3}\.\s*\d+\b', ' ', line_text)
        # Nettoie les espaces multiples et les espaces avant ponctuation
        line_text = re.sub(r'\s+', ' ', line_text).strip()
        line_text = re.sub(r'\s+([,;:.!?])', r'\1', line_text)
        if line_text:
            cleaned_lines.append(line_text)
    
    # Étape 3 : Fusion des mots coupés par un tiret
    cleaned_lines = fusionner_mots_coupes(cleaned_lines)
    
    # Étape 4 : Suppression des bruits typographiques (ex: "Sb. 03")
    cleaned_lines = supprimer_bruits_typographiques(cleaned_lines)
    
    # Étape 5 : Extraction des traductions kabyle-français
    traductions, lignes_sans_trads = extraire_traductions(cleaned_lines)
    
    # Étape 6 : Fusion intelligente des lignes courtes (1 ou 2 mots)
    merged_lines = fusionner_lignes_courtes(lignes_sans_trads)
    
    # Étape 7 : Réinsertion des traductions à la fin du texte, sous l'en-tête "# traduction"
    if traductions:
        merged_lines.append("")  # Ajoute une ligne vide pour séparer
        merged_lines.append("# traduction")
        merged_lines.extend(traductions)
    
    return "\n".join(merged_lines)

def process_directory(input_dir, output_dir):
    """
    Parcourt récursivement le répertoire 'input_dir' pour traiter tous les fichiers .md.
    Chaque fichier est nettoyé avec clean_kabyle_text_with_merge et sauvegardé dans 'output_dir'.
    """
    os.makedirs(output_dir, exist_ok=True)
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(".md"):
                input_path = os.path.join(root, filename)
                try:
                    with open(input_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"Erreur lors de la lecture de {input_path}: {e}")
                    continue
                
                cleaned = clean_kabyle_text_with_merge(content)
                output_path = os.path.join(output_dir, filename)
                try:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(cleaned)
                    print(f"Fichier traité : {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Erreur lors de l'écriture de {output_path}: {e}")

# Exemple d'utilisation :
input_directory = "./Autre/avant"  # Répertoire contenant tes fichiers .md
output_directory = "./Autre/apres"    # Répertoire de sortie pour les fichiers nettoyés

process_directory(input_directory, output_directory)
