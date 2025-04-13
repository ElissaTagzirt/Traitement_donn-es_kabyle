import os
import re
from collections import Counter
import csv

# Chemin du répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Chemin du répertoire parent à partir du répertoire du script
chemin_repertoire_parent = os.path.join(script_dir, "./Corpus_01_MohammedBelkacem/KabyleTexte/low quality_corrected/apres")

# Préfixe à supprimer dans le chemin complet
prefix_a_supprimer = "/home/elissatagzirt/Documents/code/Traitement_donnees/Git-Hub/Corpus_GitHub/"

# Nom du fichier CSV où seront sauvegardées les statistiques
nom_fichier_csv = "corrected.csv"

# Vérifier si le fichier CSV existe déjà
fichier_existe = os.path.isfile(nom_fichier_csv)

# Ouvrir le fichier CSV en mode ajout ("append")
with open(nom_fichier_csv, "a", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Si le fichier n'existe pas, écrire l'en-tête
    if not fichier_existe:
        writer.writerow([
            "Fichier ;"
            "Nombre de lignes ;"
            "Nombre total de tokens ;"
            "Moyenne de tokens par ligne ;"
            "Top 10 tokens"
        ])
    
    # Parcourir tous les sous-répertoires à partir du répertoire parent
    for racine, dossiers, fichiers in os.walk(chemin_repertoire_parent):
        for nom_fichier in fichiers:
            if nom_fichier.endswith('.md'):
                chemin_fichier = os.path.join(racine, nom_fichier)
                # Obtenir le chemin absolu pour avoir le chemin complet du fichier
                chemin_complet = os.path.abspath(chemin_fichier)
                
                # Supprimer le préfixe si le chemin commence par celui-ci
                if chemin_complet.startswith(prefix_a_supprimer):
                    # Extraire la partie du chemin après le préfixe
                    chemin_relatif = chemin_complet[len(prefix_a_supprimer):]
                    # Si cela commence par un slash, on le retire pour éviter "//"
                    if chemin_relatif.startswith("/"):
                        chemin_relatif = chemin_relatif[1:]
                else:
                    # Si le fichier n'est pas dans ce préfixe, on garde simplement le chemin absolu
                    chemin_relatif = chemin_complet

                # On lit le fichier ligne par ligne, en ne gardant que celles qui ne sont pas vides après strip()
                with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                    lignes_non_vides = [ligne for ligne in fichier if ligne.strip()]

                # Calcul du nombre de lignes (en ignorant celles qui sont vides)
                nombre_lignes = len(lignes_non_vides)
                tokens_total = []
                
                # Pour chaque ligne non vide, découper en tokens sur les espaces et les tirets
                for ligne in lignes_non_vides:
                    tokens = re.split(r'[ -]+', ligne.strip())
                    tokens = [token for token in tokens if token]
                    tokens_total.extend(tokens)
                
                # Calcul du nombre total de tokens et de la moyenne par ligne
                nombre_tokens = len(tokens_total)
                moyenne_tokens = nombre_tokens / nombre_lignes if nombre_lignes > 0 else 0
                
                # Calcul des 10 tokens les plus fréquents
                frequences = Counter(tokens_total)
                top_10 = frequences.most_common(10)
                top_10_str = "; ".join([f"{token}: {freq}" for token, freq in top_10])
                
                # Écriture des données dans le CSV
                # Chaque information est dans une colonne distincte
                writer.writerow([
                    f"{chemin_relatif} ;"
                    f"{nombre_lignes} ;"
                    f"{nombre_tokens} ;"
                    f"{moyenne_tokens:.2f} ;",
                    top_10_str
                ])

print("Les données ont été ajoutées au fichier CSV :", nom_fichier_csv)
