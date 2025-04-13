# Chemin vers ton fichier .md
file_path = "Ungalnwuccen.pdf.md"

# Lecture du fichier
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacement de tous les $ par g
content_modifié = content.replace('$', 'ɣ')

# Écriture du nouveau contenu dans le même fichier
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_modifié)

print(f"Tous les '$' ont été remplacés par 'g' dans {file_path}")
