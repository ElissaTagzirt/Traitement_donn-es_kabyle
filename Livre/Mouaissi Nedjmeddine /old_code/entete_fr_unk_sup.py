import os
import re

def process_file(filepath, headers_dir, fr_dir, clean_dir):
    """
    Pour un fichier Markdown donné, le script effectue les opérations suivantes :
      - Divise le contenu en pages à partir du marqueur "## Page X".
      - Pour chaque page, extrait :
         * Les lignes contenant "head" ou "footer" (insensible à la casse).
         * Les blocs de texte entre <fr> et </fr>.
         * Le contenu "clean" (texte sans les blocs <fr>...</fr> et sans balises <unk>).
      - Concatène les résultats en conservant le marqueur de page pour chaque section.
      - Écrit les trois contenus dans des fichiers distincts dans les répertoires indiqués.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Division du contenu en pages à partir du marqueur "## Page X"
    parts = re.split(r'(##\s*Page\s*\d+)', content, flags=re.IGNORECASE)
    
    header_results = []
    fr_results = []
    clean_results = []
    
    # Si le contenu débute par du texte avant le premier marqueur de page, on le traite comme "Page 0"
    if parts[0].strip():
        page_marker = "## Page 0"
        page_content = parts[0]
        header_results.append(page_marker)
        fr_results.append(page_marker)
        clean_results.append(page_marker)
        
        headers = re.findall(r'^(.*(?:head|footer).*)$', page_content, flags=re.IGNORECASE | re.MULTILINE)
        if headers:
            header_results.append("\n".join(headers))
        else:
            header_results.append("Aucune ligne 'head' ou 'footer' n'a été trouvée.")
        
        fr_blocks = re.findall(r'<fr>(.*?)</fr>', page_content, flags=re.DOTALL | re.IGNORECASE)
        if fr_blocks:
            fr_results.append("\n\n".join(fr_blocks))
        else:
            fr_results.append("Aucun bloc <fr>...</fr> n'a été trouvé.")
        
        clean_page = re.sub(r'<fr>.*?</fr>', '', page_content, flags=re.DOTALL | re.IGNORECASE)
        clean_page = re.sub(r'</?unk>', '', clean_page, flags=re.IGNORECASE)
        clean_results.append(clean_page)
    
    # Parcours des parties en considérant les pages (chaque marqueur suivi de son contenu)
    for i in range(1, len(parts), 2):
        page_marker = parts[i].strip()  # Ex: "## Page 1"
        page_content = parts[i+1] if i+1 < len(parts) else ""
        
        header_results.append(page_marker)
        fr_results.append(page_marker)
        clean_results.append(page_marker)
        
        headers = re.findall(r'^(.*(?:head|footer).*)$', page_content, flags=re.IGNORECASE | re.MULTILINE)
        if headers:
            header_results.append("\n".join(headers))
        else:
            header_results.append("Aucune ligne 'head' ou 'footer' n'a été trouvée.")
        
        fr_blocks = re.findall(r'<fr>(.*?)</fr>', page_content, flags=re.DOTALL | re.IGNORECASE)
        if fr_blocks:
            fr_results.append("\n\n".join(fr_blocks))
        else:
            fr_results.append("Aucun bloc <fr>...</fr> n'a été trouvé.")
        
        clean_page = re.sub(r'<fr>.*?</fr>', '', page_content, flags=re.DOTALL | re.IGNORECASE)
        clean_page = re.sub(r'</?unk>', '', clean_page, flags=re.IGNORECASE)
        clean_results.append(clean_page)
    
    # Concaténation des résultats, avec une séparation nette entre les pages
    header_output = "\n\n".join(header_results)
    fr_output = "\n\n".join(fr_results)
    clean_output = "\n\n".join(clean_results)
    
    # Construction des noms de fichiers de sortie
    base_name = os.path.splitext(os.path.basename(filepath))[0] + ".md"
    header_filename = os.path.join(headers_dir, f"header_{base_name}")
    fr_filename = os.path.join(fr_dir, f"fr_{base_name}")
    clean_filename = os.path.join(clean_dir, f"clean_{base_name}")
    
    # Écriture des fichiers résultat
    with open(header_filename, 'w', encoding='utf-8') as f_out:
        f_out.write(header_output)
    with open(fr_filename, 'w', encoding='utf-8') as f_out:
        f_out.write(fr_output)
    with open(clean_filename, 'w', encoding='utf-8') as f_out:
        f_out.write(clean_output)
    
    print(f"Traitement de '{filepath}':")
    print(f"  -> Fichier header enregistré dans '{header_filename}'")
    print(f"  -> Fichier fr enregistré dans '{fr_filename}'")
    print(f"  -> Fichier clean enregistré dans '{clean_filename}'\n")

def traverse_directory(input_directory, output_base):
    """
    Parcourt le répertoire (et ses sous‑répertoires) pour trouver tous les fichiers Markdown (.md)
    et traite chacun d'eux. Les fichiers de sortie seront créés dans trois sous‑répertoires
    (headers, fr, clean) dans le répertoire output_base.
    """
    headers_dir = os.path.join(output_base, "headers")
    fr_dir = os.path.join(output_base, "fr")
    clean_dir = os.path.join(output_base, "clean")
    
    os.makedirs(headers_dir, exist_ok=True)
    os.makedirs(fr_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith('.md'):
                filepath = os.path.join(root, file)
                process_file(filepath, headers_dir, fr_dir, clean_dir)

def main():
    input_directory = "./Markdown_tagged_roberta2/without_tables/moyennement_de_francais/pure"   # Remplacez par le chemin de votre répertoire contenant les .md
    output_base = "./Markdown_tagged_roberta2/without_tables/moyennement_de_francais"          # Répertoire de base pour les sorties

    traverse_directory(input_directory, output_base)
    print("Traitement terminé.")

if __name__ == '__main__':
    main()
