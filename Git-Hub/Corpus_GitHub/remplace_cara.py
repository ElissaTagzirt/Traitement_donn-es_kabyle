# Définissez ici le chemin de votre fichier Markdown
FILE_PATH = "./Corpus_01_MohammedBelkacem/corpus-kab/corpus-brut/idlisen/aberrani.md"


def replace_ampersand(filepath):
    try:
        # Lecture du contenu du fichier
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Remplacement de chaque "&" par "ɛ"
        new_content = content.replace("&", "ɛ")
        
        # Écriture du contenu modifié dans le même fichier (écrase l'ancien contenu)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(new_content)
        
        print(f"Les remplacements ont été effectués avec succès dans {filepath}")
    except Exception as e:
        print(f"Erreur lors du traitement du fichier : {e}")

if __name__ == "__main__":
    replace_ampersand(FILE_PATH)
