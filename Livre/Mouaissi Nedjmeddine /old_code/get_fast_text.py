import os
import requests
import fasttext

MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
MODEL_PATH = "lid.176.bin"
# Taille approximative attendue en octets (à vérifier, ici on prend 126MB environ)
EXPECTED_SIZE = 126 * 1024 * 1024

def download_fasttext_model(model_path=MODEL_PATH, url=MODEL_URL, expected_size=EXPECTED_SIZE):
    """
    Vérifie si le modèle existe et a une taille correcte.
    Si le fichier est manquant ou incomplet, le télécharge.
    """
    if os.path.exists(model_path):
        actual_size = os.path.getsize(model_path)
        if actual_size >= expected_size:
            print(f"Modèle déjà téléchargé ({actual_size} octets).")
            return
        else:
            print("Le fichier existant semble incomplet. Suppression du fichier et téléchargement en cours.")
            os.remove(model_path)
    
    print(f"Téléchargement du modèle depuis {url}...")
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')
    if total_length is None:
        with open(model_path, 'wb') as f:
            f.write(response.content)
    else:
        total_length = int(total_length)
        downloaded = 0
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    print(f"\rTéléchargé {downloaded / total_length:.2%}", end="")
    print("\nTéléchargement terminé.")

# Vérification et téléchargement du modèle
download_fasttext_model()

# Chargement du modèle FastText
try:
    model = fasttext.load_model(MODEL_PATH)
    print("Modèle FastText 'lid.176.bin' chargé avec succès.")
except Exception as e:
    print("Erreur lors du chargement du modèle :", e)
