#!/usr/bin/env python3
import os
import shutil

def read_identifiers(txt_file):
    """
    Lit le fichier txt_file contenant la liste des identifiants (un identifiant par ligne)
    et retourne un ensemble (set) d'identifiants.
    """
    if not os.path.exists(txt_file):
        return set()
    with open(txt_file, "r", encoding="utf-8") as f:
        identifiers = {line.strip() for line in f if line.strip()}
    return identifiers

def extract_files(identifiers, source_dir, target_dir):
    """
    Parcourt les fichiers dans source_dir (ici, le répertoire "dup")
    et copie ceux dont l'identifiant (la partie avant le premier '_')
    se trouve dans l'ensemble identifiers vers le répertoire target_dir.
    """
    # Créer le répertoire cible s'il n'existe pas
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    copied_count = 0
    for filename in os.listdir(source_dir):
        chemin_fichier = os.path.join(source_dir, filename)
        if os.path.isfile(chemin_fichier) and filename.lower().endswith('.pdf'):
            # Extraction de l'identifiant : la partie avant le premier underscore
            parts = filename.split('_')
            if parts:
                file_id = parts[0]
                if file_id in identifiers:
                    shutil.copy(chemin_fichier, os.path.join(target_dir, filename))
                    print(f"{filename} a été copié dans {target_dir}.")
                    copied_count += 1
    print(f"{copied_count} fichiers ont été copiés dans {target_dir}.")

def main():
    # Fichier contenant les identifiants extraits (un par ligne)
    identifiers_file = "identifiants.txt"
    # Répertoire source contenant les fichiers à extraire
    source_dir = "./PDFs/dup"
    # Répertoire cible où copier les fichiers sélectionnés
    target_dir = "./PDFs/imp/with_tables"
    
    # Lecture des identifiants
    identifiers = read_identifiers(identifiers_file)
    if not identifiers:
        print(f"Aucun identifiant trouvé dans le fichier {identifiers_file}.")
        return
    
    print(f"Identifiants lus : {identifiers}")
    extract_files(identifiers, source_dir, target_dir)

if __name__ == '__main__':
    main()
