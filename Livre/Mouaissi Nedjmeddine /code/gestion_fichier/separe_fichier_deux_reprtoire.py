import os
import shutil

def charger_noms_traite(fichier_liste):
    with open(fichier_liste, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def separer_pdfs(dossier_pdf, fichier_liste, dossier_sortie_traite, dossier_sortie_non_traite):
    noms_traite = charger_noms_traite(fichier_liste)

    if not os.path.exists(dossier_sortie_traite):
        os.makedirs(dossier_sortie_traite)
    if not os.path.exists(dossier_sortie_non_traite):
        os.makedirs(dossier_sortie_non_traite)

    for nom_fichier in os.listdir(dossier_pdf):
        if not nom_fichier.lower().endswith(".md"):
            continue
        nom_sans_ext = os.path.splitext(nom_fichier)[0]
        chemin_source = os.path.join(dossier_pdf, nom_fichier)

        if nom_sans_ext in noms_traite:
            chemin_dest = os.path.join(dossier_sortie_traite, nom_fichier)
        else:
            chemin_dest = os.path.join(dossier_sortie_non_traite, nom_fichier)

        shutil.copy2(chemin_source, chemin_dest)

    print("Séparation terminée.")

# === Paramètres ===
DOSSIER_PDF = "../../data/pdfs_etat_1_markdown/text_selectable/"
FICHIER_LISTE = "fichiers_vides.txt"
DOSSIER_TRAITE = "../../data/pdfs_etat_1_markdown/text_selectable/traite"
DOSSIER_NON_TRAITE = "../../data/pdfs_etat_1_markdown/text_selectable/non_traite"

# === Lancement ===
separer_pdfs(DOSSIER_PDF, FICHIER_LISTE, DOSSIER_TRAITE, DOSSIER_NON_TRAITE)
