import os
import re
import numpy as np
import shutil

def compute_french_ratio(filepath):
    """
    Lit le fichier Markdown, compte le nombre total de mots et ceux situés
    entre <fr>...</fr>, puis calcule le ratio de contenu français.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    total_words = len(re.findall(r'\w+', text))
    french_segments = re.findall(r'<fr>(.*?)</fr>', text, flags=re.DOTALL)
    french_words = sum(len(re.findall(r'\w+', segment)) for segment in french_segments)
    ratio = french_words / total_words if total_words else 0
    return ratio

def traverse_directory(directory):
    """
    Parcourt le répertoire et ses sous-dossiers pour trouver les fichiers Markdown (.md),
    calcule le ratio de contenu français pour chacun et retourne une liste de ratios et 
    la liste correspondante des chemins de fichiers.
    """
    ratios = []
    file_names = []
    for root, dirs, files in os.walk(directory):
        # Exclure les sous-dossiers de sortie pour éviter de retraiter les fichiers déplacés
        dirs[:] = [d for d in dirs if d not in {"peu_de_francais", "moyennement_de_francais", "beaucoup_de_francais"}]
        for file in files:
            if file.lower().endswith('.md'):
                filepath = os.path.join(root, file)
                ratio = compute_french_ratio(filepath)
                ratios.append(ratio)
                file_names.append(filepath)
    return ratios, file_names

def separate_files_by_category(ratios, file_names):
    """
    Sépare les fichiers en trois catégories selon :
    - "peu de français" pour les fichiers dont le ratio est inférieur au 25e percentile (Q1)
    - "moyennement de français" pour ceux dont le ratio est entre Q1 et Q3
    - "beaucoup de français" pour ceux dont le ratio est supérieur au 75e percentile (Q3)
    """
    q1 = np.percentile(ratios, 25)
    q3 = np.percentile(ratios, 75)
    
    category_low = []   # peu de français
    category_mid = []   # moyennement de français
    category_high = []  # beaucoup de français
    
    for file, ratio in zip(file_names, ratios):
        if ratio < q1:
            category_low.append(file)
        elif ratio > q3:
            category_high.append(file)
        else:
            category_mid.append(file)
    
    print(f"Seuils calculés : Q1 (25e percentile) = {q1:.2%} et Q3 (75e percentile) = {q3:.2%}")
    return category_low, category_mid, category_high

def move_files_to_categories(category_low, category_mid, category_high, directory):
    """
    Déplace les fichiers dans trois sous-dossiers distincts situés dans le répertoire donné.
    """
    low_dir = os.path.join(directory, "peu_de_francais")
    mid_dir = os.path.join(directory, "moyennement_de_francais")
    high_dir = os.path.join(directory, "beaucoup_de_francais")
    os.makedirs(low_dir, exist_ok=True)
    os.makedirs(mid_dir, exist_ok=True)
    os.makedirs(high_dir, exist_ok=True)
    
    for file in category_low:
        shutil.move(file, os.path.join(low_dir, os.path.basename(file)))
    for file in category_mid:
        shutil.move(file, os.path.join(mid_dir, os.path.basename(file)))
    for file in category_high:
        shutil.move(file, os.path.join(high_dir, os.path.basename(file)))
    
    print("Les fichiers ont été déplacés dans les sous-répertoires du répertoire :", directory)

def main():
    directory = "./Markdown_tagged_roberta2/without_tables"
    ratios, file_names = traverse_directory(directory)
    
    # Affichage des ratios pour chaque fichier
    print("Ratios de contenu français par fichier :")
    for file, ratio in zip(file_names, ratios):
        print(f"{file}: {ratio:.2%}")
    
    # Séparation des fichiers en 3 catégories
    category_low, category_mid, category_high = separate_files_by_category(ratios, file_names)
    
    # Affichage de la liste des fichiers par catégorie
    print("\nCatégorie 'peu de français':")
    for file in category_low:
        print(f"  - {file}")
    
    print("\nCatégorie 'moyennement de français':")
    for file in category_mid:
        print(f"  - {file}")
    
    print("\nCatégorie 'beaucoup de français':")
    for file in category_high:
        print(f"  - {file}")
    
    # Affichage du nombre de fichiers dans chaque catégorie
    print("\nNombre de fichiers par catégorie :")
    print(f"  Peu de français        : {len(category_low)} fichier(s)")
    print(f"  Moyennement de français: {len(category_mid)} fichier(s)")
    print(f"  Beaucoup de français   : {len(category_high)} fichier(s)")
    
    # Déplacement des fichiers dans les sous-dossiers correspondants
    move_files_to_categories(category_low, category_mid, category_high, directory)

if __name__ == '__main__':
    main()
