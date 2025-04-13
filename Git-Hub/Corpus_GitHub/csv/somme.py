import csv
import glob
import re

total_lignes = 0
total_tokens = 0

for filepath in glob.glob("*.csv"):
    print(f"Traitement du fichier : {filepath}")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  # Sauter l'en-tête
        for row in reader:
            try:
                # Extraction de la valeur numérique pour la 2ème colonne
                value_lignes = row[1]
                match_lignes = re.search(r'\d+', value_lignes)
                if match_lignes:
                    total_lignes += int(match_lignes.group(0))
                else:
                    print(f"Aucun nombre trouvé dans la 2ème colonne du fichier {filepath}: {value_lignes}")

                # Extraction de la valeur numérique pour la 3ème colonne
                value_tokens = row[2]
                match_tokens = re.search(r'\d+', value_tokens)
                if match_tokens:
                    total_tokens += int(match_tokens.group(0))
                else:
                    print(f"Aucun nombre trouvé dans la 3ème colonne du fichier {filepath}: {value_tokens}")

            except Exception as e:
                print(f"Erreur de traitement dans le fichier {filepath}: {e}")

print("Somme totale de la 2ème colonne (Nombre de lignes):", total_lignes)
print("Somme totale de la 3ème colonne (Nombre total de tokens):", total_tokens)
