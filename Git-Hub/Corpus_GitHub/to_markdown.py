import os
import csv

# Définissez ici le chemin du répertoire parent à parcourir
PARENT_DIRECTORY = "./Corpus_07_Ziri Sut"

def convert_txt_to_md(txt_filepath, md_filepath):
    """
    Lit un fichier .txt et écrit son contenu dans un fichier .md.
    Vous pouvez ajouter ici des transformations pour adapter le format Markdown.
    """
    try:
        with open(txt_filepath, "r", encoding="utf-8") as file:
            content = file.read()
        with open(md_filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Conversion réussie : {txt_filepath} -> {md_filepath}")
    except Exception as e:
        print(f"Erreur lors de la conversion de {txt_filepath} : {e}")

def convert_csv_to_md(csv_filepath, md_filepath):
    """
    Lit un fichier .csv et le convertit en un format type tableau Markdown,
    sans utiliser le caractère '|' pour délimiter les colonnes.
    La première ligne est considérée comme l'entête.
    """
    try:
        with open(csv_filepath, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
        if not rows:
            print(f"{csv_filepath} est vide.")
            return
        
        # Construction du "tableau" Markdown sans les '|'
        header = rows[0]
        table_lines = []
        # Ligne d'entête sans '|'
        table_lines.append(" ".join(header))
        # Ligne de séparation (on utilise '---' pour chaque colonne)
        table_lines.append(" ".join(["---"] * len(header)))
        # Lignes de données
        for row in rows[1:]:
            table_lines.append(" ".join(row))
        
        md_content = "\n".join(table_lines)
        with open(md_filepath, "w", encoding="utf-8") as file:
            file.write(md_content)
        print(f"Conversion réussie : {csv_filepath} -> {md_filepath}")
    except Exception as e:
        print(f"Erreur lors de la conversion de {csv_filepath} : {e}")

def traverse_and_convert(parent_directory):
    """
    Parcourt récursivement le répertoire parent et tous ses sous-répertoires.
    Pour chaque fichier .txt ou .csv trouvé, effectue la conversion en Markdown.
    """
    for dirpath, _, filenames in os.walk(parent_directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            basename, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext == ".txt":
                md_filepath = os.path.join(dirpath, basename + ".md")
                convert_txt_to_md(filepath, md_filepath)
            elif ext == ".csv":
                md_filepath = os.path.join(dirpath, basename + ".md")
                convert_csv_to_md(filepath, md_filepath)

if __name__ == "__main__":
    traverse_and_convert(PARENT_DIRECTORY)
