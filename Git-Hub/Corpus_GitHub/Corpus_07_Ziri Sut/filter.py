import csv
import os

# Nom du fichier CSV en entrée et en sortie
input_file = 'Corpus_07_Ziri Sut.csv'
output_file = 'Corpus_07_Ziri Sut_save.csv'

with open(input_file, newline='', encoding='utf-8') as csv_in:
    reader = csv.reader(csv_in)
    rows = list(reader)

# On suppose que la première ligne contient les en-têtes
header = rows[0]
header.append('Fichier')  # Ajout de la nouvelle colonne
output_rows = [header]

# Parcours des lignes à partir de la deuxième (les données)
for row in rows[1:]:
    # Récupérer le chemin à partir de la première colonne (indice 0)
    chemin = row[0]
    
    # Si le chemin contient '/.git', on ignore cette ligne
    if '/.git' in chemin:
        continue

    premiere_ligne = ''
    if os.path.exists(chemin):
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                premiere_ligne = f.readline().strip()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {chemin} : {e}")
    else:
        print(f"Le fichier {chemin} n'existe pas.")
    
    # Ajout de la première ligne du fichier dans la nouvelle colonne
    row.append(premiere_ligne)
    output_rows.append(row)

with open(output_file, 'w', newline='', encoding='utf-8') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(output_rows)
