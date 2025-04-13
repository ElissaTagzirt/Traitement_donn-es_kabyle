import os

# Définissez ici le chemin du répertoire parent à parcourir
PARENT_DIRECTORY = "./Corpus_07_Ziri Sut"

def delete_txt_files(root_directory):
    """
    Parcourt récursivement le répertoire et supprime tous les fichiers se terminant par '.txt'.
    """
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith(".txt"):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"Fichier supprimé : {file_path}")
                except Exception as e:
                    print(f"Erreur lors de la suppression de {file_path} : {e}")

if __name__ == "__main__":
    delete_txt_files(PARENT_DIRECTORY)
