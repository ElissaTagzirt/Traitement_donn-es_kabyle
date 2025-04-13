import os
import shutil

# Chemin du répertoire contenant les fichiers PDF
repertoire_pdf = "./PDFs/non_imp/without_tables"  # À modifier selon votre chemin

# Chemin du fichier contenant les identifiants traités
chemin_identifiants = "identifiants.txt"

# Création des répertoires pour les fichiers traités et non traités
repertoire_traite = os.path.join(repertoire_pdf, "moyennement_de_francais")
repertoire_non_traite = os.path.join(repertoire_pdf, "Autre")

os.makedirs(repertoire_traite, exist_ok=True)
os.makedirs(repertoire_non_traite, exist_ok=True)

# Lecture des identifiants déjà traités depuis le fichier
identifiants_traite = set()
with open(chemin_identifiants, "r", encoding="utf-8") as f:
    for ligne in f:
        id_ligne = ligne.strip()
        if id_ligne:
            identifiants_traite.add(id_ligne)

# Parcours des fichiers du répertoire
for fichier in os.listdir(repertoire_pdf):
    # On ne traite que les fichiers se terminant par .pdf
    if fichier.endswith(".pdf"):
        # Extraction de l'identifiant : nombre avant le "_"
        identifiant = fichier.split("_")[0]
        chemin_fichier = os.path.join(repertoire_pdf, fichier)
        
        # Déplacement selon si l'identifiant a déjà été traité ou non
        if identifiant in identifiants_traite:
            destination = os.path.join(repertoire_traite, fichier)
        else:
            destination = os.path.join(repertoire_non_traite, fichier)
        
        shutil.move(chemin_fichier, destination)

print("Séparation des fichiers terminée.")
