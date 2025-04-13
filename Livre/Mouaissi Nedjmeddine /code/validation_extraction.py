import os
import re


def lister_noms_sans_extension(dossier):
    noms_sans_ext = []
    for nom_fichier in os.listdir(dossier):
        chemin_complet = os.path.join(dossier, nom_fichier)
        if os.path.isfile(chemin_complet):
            nom_sans_ext = os.path.splitext(nom_fichier)[0]
            noms_sans_ext.append(nom_sans_ext)
    return noms_sans_ext


def heuristique_extraction_valide(contenu):
    """
    Vérifie si le contenu extrait semble valide :
    - Rejette si des caractères ou mots indiquent un mauvais encodage ou une corruption
    - Rejette si mots collés sans espace ou répétitions anormales
    - Rejette si des artefacts (cid:xxx) apparaissent (signe de mauvais encodage PDF)
    """
    lignes = contenu.strip().split("\n")
    texte_total = " ".join(lignes)

    # Caractères suspects
    caracteres_suspects = ["ê", "ù", "î", "ç", "$", "&"]
    if any(c in texte_total for c in caracteres_suspects):
        return False

    # Séquences de type (cid:xxx) → problème d'encodage PDF
    if re.search(r"\(cid:[0-9]+\)", texte_total):
        return False

    # Mots collés sans espace (phrases longues sans ponctuation)
    mots_collés = re.findall(r'\b\w{30,}\b', texte_total)
    if mots_collés:
        return False

    # Répétitions excessives de lettres ou séquences bizarres
    if re.search(r'(\w)\1{4,}', texte_total):  # ex : aaaa, eeeee, ssssss
        return False


    return True


def verifier_et_classer_md(dossier_md, dossier_ok, dossier_a_revoir):
    if not os.path.exists(dossier_ok):
        os.makedirs(dossier_ok)
    if not os.path.exists(dossier_a_revoir):
        os.makedirs(dossier_a_revoir)

    for fichier in os.listdir(dossier_md):
        if not fichier.endswith(".md"):
            continue
        chemin_complet = os.path.join(dossier_md, fichier)
        with open(chemin_complet, "r", encoding="utf-8") as f:
            contenu = f.read()
        if heuristique_extraction_valide(contenu):
            dest = os.path.join(dossier_ok, fichier)
        else:
            dest = os.path.join(dossier_a_revoir, fichier)
        os.rename(chemin_complet, dest)


# Exemple d'utilisation :
repertoire = "../data/pdfs_etat_0/text_selectable"
noms_fichiers = lister_noms_sans_extension(repertoire)

fichier_sortie = "liste_fichiers_sans_extension.txt"
with open(fichier_sortie, "w", encoding="utf-8") as f:
    for nom in noms_fichiers:
        f.write(nom + "\n")

print(f"{len(noms_fichiers)} noms de fichiers sauvegardés dans {fichier_sortie}")

# Vérification des fichiers Markdown extraits
repertoire_md = "../data/pdfs_etat_1_markdown/text_selectable/lot1"
dossier_etape_suivante = "../data/pdfs_etat_2_separation/lot1/valide"
dossier_a_revoir = "../data/pdfs_etat_2_separation/lot1/a_revoir"
verifier_et_classer_md(repertoire_md, dossier_etape_suivante, dossier_a_revoir)
