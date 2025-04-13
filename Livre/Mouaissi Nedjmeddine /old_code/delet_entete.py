import os
import re

def extract_footers_from_file(filepath):
    """
    Lit un fichier Markdown et extrait toutes les lignes contenant "footer".
    Le filtrage se fait en recherchant "footer" dans chaque ligne (insensible à la casse).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    # Recherche toutes les lignes contenant "footer"
    pattern = re.compile(r'^(.*footer.*)$', re.MULTILINE | re.IGNORECASE)
    footers = pattern.findall(text)
    return footers

def traverse_and_extract(directory, output_directory):
    """
    Parcourt le répertoire et ses sous-dossiers pour traiter les fichiers Markdown.
    Pour chaque fichier, extrait les lignes contenant "footer" et les écrit dans un nouveau fichier
    dans le dossier output_directory. Le nouveau fichier est nommé "footer_<nom_fichier>.md".
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.md'):
                filepath = os.path.join(root, file)
                footers = extract_footers_from_file(filepath)
                if footers:
                    # Création du nom du fichier de sortie
                    base_name = os.path.splitext(file)[0]
                    output_file_name = f"footer_{base_name}.md"
                    output_path = os.path.join(output_directory, output_file_name)
                    with open(output_path, 'w', encoding='utf-8') as out:
                        out.write("\n".join(footers))
                    print(f"Footers extraites de '{filepath}' et sauvegardées dans '{output_path}'.")
                else:
                    print(f"Aucun footer trouvé dans '{filepath}'.")

def main():
    input_directory = "./Markdown_tagged_roberta/without_tables"
    output_directory = "./extracted_footers"
    traverse_and_extract(input_directory, output_directory)

if __name__ == '__main__':
    main()
