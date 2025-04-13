import re

# Spécifie le fichier à nettoyer
file_path = "Tazrawt takennit n tmacahut(Agmar d userwes) gar snat n temnaḍin.pdf2.md"

# Lecture du contenu
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Nettoyages :
# 1. Supprimer les points de suspension exagérés
content = re.sub(r'[\.…]{2,}', '…', content)

# 2. Corriger les lettres répétées abusivement (ex: Prǧtttt → Prǧt)
content = re.sub(r'([A-Za-zḍẓǧɣ]+)\1{2,}', r'\1', content)

# 3. Ajouter un espace après les numéros/sous-sections (ex: a/ → a /)
content = re.sub(r'([a-zA-Z0-9])/', r'\1 /', content)

# 4. Nettoyer les espaces excessifs
content = re.sub(r'[ \t]{2,}', ' ', content)

# 5. Supprimer les lignes entièrement vides répétées
content = re.sub(r'\n{3,}', '\n\n', content)

# 6. Supprimer les caractères indésirables spécifiques si nécessaire
content = content.replace('’', '')  # facultatif, si toujours non désiré

# Écriture du fichier nettoyé
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Le fichier {file_path} a été nettoyé avec succès.")
