import os
import re

def should_include_line(line: str) -> bool:
    """
    Heuristique pour décider si une ligne doit être conservée pour l'entraînement d'un LLM.
    On exclut par exemple :
      - Les lignes vides ou trop courtes (< 5 caractères après nettoyage).
      - Les lignes composées uniquement de chiffres ou de symboles.
      - Les lignes contenant des URLs ou des liens.
      - Les lignes contenant des balises HTML.
      - Les lignes comportant des termes ou motifs spécifiques indésirables (ex. HEADER, Corpus, p(5), etc.).
    """
    stripped = line.strip()
    if not stripped:
        return False

    # Lignes trop courtes
    if len(stripped) < 3:
        return False

    # Lignes composées uniquement de chiffres et symboles
    if re.fullmatch(r'[\d\W_]+', stripped):
        return False

    # Lignes contenant des URLs ou des liens
    if re.search(r'https?://', line) or re.search(r'www\.', line):
        return False

    # Lignes contenant des balises HTML ou similaires
    if re.search(r'<\s*\/?\s*\w+\s*.*?>', line):
        return False

    # Lignes avec certains mots ou motifs à exclure (HEADER, Corpus, p(chiffre), etc.)
    if re.search(r'\bHEADER\b', line, flags=re.IGNORECASE) or re.search(r'\bCorpus\b', line, flags=re.IGNORECASE):
        return False
    if re.search(r'\bp\(\d+\)', line, flags=re.IGNORECASE):
        return False

    # On peut ajouter d'autres critères (ex. ratio lettres/chiffres, détection de langage, etc.)
    return True

def clean_line(line: str) -> str:
    """
    Applique diverses transformations pour normaliser la ligne.
    """
    new_line = line.replace("Extrait", "Tukkist")
    new_line = new_line.replace("mais", "maca")
    new_line = re.sub(r'\s*\$\s*', 'ɣ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'l\s*\’\s*usine', 'luzin', new_line, flags=re.UNICODE)
    new_line = re.sub(r'ê', 'ḥ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'è', 'A', new_line, flags=re.UNICODE)
    new_line = re.sub(r'Ö', 'Ṛ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'Ë', 'ḥ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'Ê', 'ḥ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'ç', 'č', new_line, flags=re.UNICODE)
    new_line = re.sub(r'î', 'ṭ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'Ï', 'ṭ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'O', 'Ǧ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'Ä', 'Ɛ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'1r', 'Ar', new_line, flags=re.UNICODE)
    new_line = re.sub(r'\‘', '', new_line, flags=re.UNICODE)
    new_line = new_line.replace("", "ɛ")  # Remplacement du caractère spécial par 'ɛ'
    new_line = re.sub(r'   ɣer\b', ' ɣer', new_line, flags=re.UNICODE)
    new_line = re.sub(r'(?<=[a-zA-Z])ɣef', r' ɣef', new_line, flags=re.UNICODE)
    new_line = re.sub(r'é', 'ẓ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'v', 'ḍ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'£', 'Ɣ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'û', 'ṣ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'o', 'ǧ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'ô', 'ṛ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'p', 'tt', new_line, flags=re.UNICODE)
    new_line = re.sub(r'ee', 'ɛe', new_line, flags=re.UNICODE)
    new_line = re.sub(r'Ç', 'č', new_line, flags=re.UNICODE)
    new_line = re.sub(r'ç', 'č', new_line, flags=re.UNICODE)
    new_line = re.sub(r'â', 'ɛ', new_line, flags=re.UNICODE)
    new_line = re.sub(r'\bnneɣ(?=\S)', r'nneɣ ', new_line)
    new_line = new_line.replace("\uf0a5", "ɛ")
    new_line = new_line.replace("(", "").replace(")", "")
    new_line = re.sub(r'\bneɣ([a-zA-Z]+)', r'neɣ \1', new_line)
    new_line = re.sub(r'ea', 'ɛa', new_line, flags=re.UNICODE)
    new_line = re.sub(r'La\s+poésie', "Tamedyazt n ", new_line, flags=re.IGNORECASE)
    new_line = re.sub(r'interpréter\s+par', "Ttwasefser seɣur", new_line, flags=re.IGNORECASE)
    new_line = re.sub(r'\(\s*pp\s*\.\s*\d+\s*-\s*\d+\s*\)', '', new_line, flags=re.IGNORECASE)
    new_line = re.sub(r"\(\s*p\.\s*\d+\s*\)", "", new_line)
    new_line = re.sub(r'\(\s*\d+\s*\)\s', '', new_line)
    new_line = re.sub(r'\d+\s*\.\s*', '-', new_line)
    return new_line

def filter_file(input_path: str, output_path: str):
    """
    Lit le fichier d'entrée, filtre chaque ligne selon l'heuristique et effectue les transformations,
    puis écrit le résultat dans le fichier de sortie.
    """
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    filtered_lines = []
    for line in lines:
        if should_include_line(line):
            filtered_lines.append(clean_line(line))
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(filtered_lines)

def process_directory(input_dir: str, output_dir: str):
    """
    Parcourt tous les fichiers dans le répertoire d'entrée et applique le filtrage à chacun.
    Les fichiers filtrés sont enregistrés dans le répertoire de sortie en conservant le nom original.
    """
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)
        if os.path.isfile(input_file):
            output_file = os.path.join(output_dir, filename)
            filter_file(input_file, output_file)
            print(f"Fichier traité : {filename}")

def main():
    input_dir = "./Autre/apres_filtering_etape_4"   # Répertoire contenant les fichiers à traiter
    output_dir = "./Autre/apres_filtering_etape_5"  # Répertoire pour enregistrer les fichiers nettoyés
    process_directory(input_dir, output_dir)
    print("Traitement terminé pour tous les fichiers.")

if __name__ == '__main__':
    main()
