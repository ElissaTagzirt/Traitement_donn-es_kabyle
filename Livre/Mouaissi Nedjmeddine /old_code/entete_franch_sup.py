import os
import re

def process_file(filepath, headers_dir, french_dir, clean_dir):
    """
    Pour un fichier Markdown donné, extrait :
      - Le contenu "clean" (sans blocs <french>...</french>)
      - Les lignes contenant "head" ou "footer" (insensible à la casse)
      - Les blocs de texte entre <french> et </french>
    Puis écrit ces contenus dans trois fichiers séparés dans les répertoires fournis.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraction des blocs <french>...</french>
    french_blocks = re.findall(r'<french>(.*?)</french>', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Création du contenu "clean" : suppression des blocs <french>...</french>
    clean_content = re.sub(r'<french>.*?</french>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Extraction des lignes contenant "head" ou "footer"
    # On recherche dans chaque ligne la présence de "head" ou "footer"
    header_lines = re.findall(r'^(.*(?:head|footer).*)$', content, flags=re.IGNORECASE | re.MULTILINE)
    
    # Noms de fichiers de sortie basés sur le nom de base du fichier source
    base_name = os.path.splitext(os.path.basename(filepath))[0] + ".md"
    header_filename = os.path.join(headers_dir, f"header_{base_name}")
    french_filename = os.path.join(french_dir, f"french_{base_name}")
    clean_filename  = os.path.join(clean_dir, f"clean_{base_name}")
    
    # Écriture du fichier header (les lignes extraites)
    with open(header_filename, 'w', encoding='utf-8') as f_out:
        if header_lines:
            f_out.write("\n".join(header_lines))
        else:
            f_out.write("Aucune ligne 'head' ou 'footer' n'a été trouvée.")
    
    # Écriture du fichier french (les blocs extraits)
    with open(french_filename, 'w', encoding='utf-8') as f_out:
        if french_blocks:
            # On sépare les blocs par deux retours à la ligne pour plus de lisibilité
            f_out.write("\n\n".join(french_blocks))
        else:
            f_out.write("Aucun bloc <french>...</french> n'a été trouvé.")
    
    # Écriture du fichier clean (contenu sans blocs <french>)
    with open(clean_filename, 'w', encoding='utf-8') as f_out:
        f_out.write(clean_content)
    
    print(f"Traitement de '{filepath}':")
    print(f"  -> Fichier header enregistré dans '{header_filename}'")
    print(f"  -> Fichier french enregistré dans '{french_filename}'")
    print(f"  -> Fichier clean enregistré dans '{clean_filename}'\n")

def traverse_directory(input_directory, output_base):
    """
    Parcourt le répertoire (et ses sous‑répertoires) pour trouver tous les fichiers Markdown (.md)
    et traite chacun d'eux. Les fichiers de sortie seront créés dans trois sous‑répertoires
    (headers, french, clean) dans le répertoire output_base.
    """
    headers_dir = os.path.join(output_base, "headers")
    french_dir = os.path.join(output_base, "french")
    clean_dir  = os.path.join(output_base, "clean")
    
    os.makedirs(headers_dir, exist_ok=True)
    os.makedirs(french_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith('.md'):
                filepath = os.path.join(root, file)
                process_file(filepath, headers_dir, french_dir, clean_dir)

def main():
    input_directory = "./Markdown_tagged_roberta/with_tables/beaucoup_de_francais"   # Remplacez par le chemin de votre répertoire contenant les .md
    output_base = "./Markdown_tagged_roberta/with_tables/beaucoup_de_francais" \
    ""          # Répertoire de base pour les sorties         

    traverse_directory(input_directory, output_base)
    print("Traitement terminé.")

if __name__ == '__main__':
    main()


