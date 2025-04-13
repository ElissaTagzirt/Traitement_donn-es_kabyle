import os
import fitz  # PyMuPDF
import shutil

def detect_and_separate_pdfs(folder_path):
    """
    Classe les PDF d'un dossier en deux catégories : avec texte sélectionnable et nécessitant un OCR.
    Les fichiers sont déplacés dans deux sous-dossiers : 'text_selectable/' et 'need_ocr/'.

    Paramètre :
    ----------
    folder_path : str
        Chemin du dossier contenant les fichiers PDF.
    """
    # Création des deux sous-dossiers (s'ils n'existent pas déjà)
    selectable_dir = os.path.join(folder_path, "text_selectable")
    ocr_dir = os.path.join(folder_path, "need_ocr")

    os.makedirs(selectable_dir, exist_ok=True)
    os.makedirs(ocr_dir, exist_ok=True)

    # Parcours des fichiers du dossier
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)

            # Vérification : ce n’est pas un des sous-dossiers
            if os.path.isfile(file_path):
                try:
                    doc = fitz.open(file_path)
                    text_found = False

                    # Recherche de texte sur chaque page
                    for page in doc:
                        text = page.get_text().strip()
                        if text:
                            text_found = True
                            break
                    doc.close()

                    # Déplacement dans le bon dossier
                    if text_found:
                        shutil.move(file_path, os.path.join(selectable_dir, filename))
                        print(f" {filename} → texte détecté → déplacé dans 'text_selectable/'")
                    else:
                        shutil.move(file_path, os.path.join(ocr_dir, filename))
                        print(f"🔎 {filename} → pas de texte → déplacé dans 'need_ocr/'")

                except Exception as e:
                    print(f"Erreur lors du traitement de {filename} : {e}")
                    shutil.move(file_path, os.path.join(ocr_dir, filename))

# Exemple d'utilisation :
if __name__ == "__main__":
    dossier = "../data"  
    detect_and_separate_pdfs(dossier)
