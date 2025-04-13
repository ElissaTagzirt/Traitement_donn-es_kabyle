import os

def extraire_fichiers_vides(chemin_dossier, fichier_sortie):
    """
    Parcourt le dossier indiqué et extrait le nom des fichiers vides.
    Le résultat est sauvegardé dans le fichier de sortie (un nom de fichier par ligne).
    
    :param chemin_dossier: chemin du dossier à scanner
    :param fichier_sortie: chemin du fichier texte où seront écrits les noms des fichiers vides
    """
    fichiers_vides = []
    
    # On parcourt tous les éléments du dossier
    for nom in os.listdir(chemin_dossier):
        chemin_fichier = os.path.join(chemin_dossier, nom)
        # On vérifie s'il s'agit d'un fichier (pas d'un dossier) et si sa taille est 0
        if os.path.isfile(chemin_fichier) and os.path.getsize(chemin_fichier) == 0:
            fichiers_vides.append(nom)
    
    # Écriture des noms de fichiers vides dans le fichier de sortie
    with open(fichier_sortie, "w", encoding="utf-8") as f:
        for nom_fichier in fichiers_vides:
            f.write(nom_fichier + "\n")
    
    print(f"{len(fichiers_vides)} fichiers vides trouvés dans '{chemin_dossier}'.")
    print(f"Liste sauvegardée dans '{fichier_sortie}'.")

if __name__ == "__main__":
    dossier = "./data/pdfs_etat_1_markdownllm/text_selectable"
    # Vous pouvez modifier le nom du fichier de sortie si besoin
    fichier_sortie = "fichiers_vides.txt"
    extraire_fichiers_vides(dossier, fichier_sortie)
