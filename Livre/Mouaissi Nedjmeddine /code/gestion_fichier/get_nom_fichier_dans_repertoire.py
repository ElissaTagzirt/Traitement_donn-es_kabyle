
import os

def lister_noms_sans_extension(dossier):
    noms_sans_ext = []
    for nom_fichier in os.listdir(dossier):
        chemin_complet = os.path.join(dossier, nom_fichier)
        if os.path.isfile(chemin_complet):
            nom_sans_ext = os.path.splitext(nom_fichier)[0]
            noms_sans_ext.append(nom_sans_ext)
    return noms_sans_ext

# Exemple d'utilisation :
repertoire = "../../data/pdfs_etat_1_markdown/text_selectable"
noms_fichiers = lister_noms_sans_extension(repertoire)

# Sauvegarde dans un fichier texte
fichier_sortie = "liste_fichiers_sans_extension.txt"
with open(fichier_sortie, "w", encoding="utf-8") as f:
    for nom in noms_fichiers:
        f.write(nom + "\n")

print(f"{len(noms_fichiers)} noms de fichiers sauvegardés dans {fichier_sortie}")
