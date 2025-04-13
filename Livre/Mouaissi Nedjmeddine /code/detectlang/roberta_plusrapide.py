import os
import logging
import nltk
from transformers import pipeline
from nltk.tokenize import wordpunct_tokenize
from tqdm import tqdm  # Nécessite l'installation via "pip install tqdm"

# Télécharger la ressource NLTK 'punkt' nécessaire pour le tokenizing
nltk.download('punkt')

# Configuration du logging pour afficher les messages dans la console et les enregistrer dans un fichier
logging.basicConfig(
    level=logging.INFO,  # Affiche les messages d'info et plus
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format de date, niveau et message
    handlers=[
        logging.FileHandler("process_log.log"),  # Enregistrement dans un fichier
        logging.StreamHandler()  # Affichage dans la console
    ]
)

# Forcer l'utilisation du CPU uniquement
# Avec Transformers, device = -1 signifie utiliser le CPU (aucun GPU n'est exploité)
device = -1
logging.info("Utilisation du GPU: Non (mode CPU uniquement)")

# Chargement du pipeline de détection de langue avec le modèle choisi
# Le pipeline "text-classification" est utilisé pour la détection de langue
lang_detector = pipeline(
    "text-classification",
    model="papluca/xlm-roberta-base-language-detection",
    device=device
)

# Seuil de confiance : pour considérer qu'une détection est fiable
CONFIDENCE_THRESHOLD = 0.5

def process_file(input_filepath, output_filepath):
    """
    Traite un fichier Markdown pour détecter la langue des lignes et des mots.
    
    1. Les lignes en-tête (commençant par "#") et les lignes vides sont ignorées.
    2. Une détection globale est réalisée sur chaque ligne non ignorée.
    3. Pour les lignes dont le résultat de la détection n'est pas concluant,
       une détection au niveau de chaque token est effectuée (en batch).
    4. Chaque token jugé français (selon le seuil) est entouré de balises <fr>...</fr>.
    5. Le fichier traité est sauvegardé sur le chemin indiqué.
    """
    logging.info(f"Traitement du fichier : {input_filepath}")
    
    # Lecture du fichier en mode lecture avec encodage UTF-8
    with open(input_filepath, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    # Initialisation de deux listes : indices des lignes à traiter et leur contenu
    indices_to_process = []
    non_header_lines = []
    
    # Parcours de chaque ligne avec son indice
    for i, line in enumerate(lines):
        # Ignorer les lignes qui commencent par "#" ou qui sont vides
        if line.lstrip().startswith("#") or not line.strip():
            continue
        indices_to_process.append(i)
        # Supprimer les espaces de début et de fin pour traitement ultérieur
        non_header_lines.append(line.strip())

    # Application du pipeline de détection sur l'ensemble des lignes sélectionnées (traitement en batch)
    batch_results = lang_detector(non_header_lines, truncation=True) if non_header_lines else []
    
    # Création d'une copie des lignes originales pour modification ultérieure
    processed_lines = lines.copy()

    # Pour chaque ligne traitée, appliquer les modifications si elle est considérée comme du français
    for idx, result in zip(indices_to_process, batch_results):
        # Récupérer l'étiquette et le score en nettoyant le label (suppression du préfixe '__label__')
        label = result.get('label', '').replace('__label__', '')
        score = result.get('score', 0.0)

        # Si la détection globale estime que la ligne est en français avec un score suffisant
        if label == 'fr' and score >= CONFIDENCE_THRESHOLD:
            # Encadrer la ligne complète avec des balises <fr>...</fr>
            processed_lines[idx] = f"<fr>{lines[idx].strip()}</fr>\n"

        # Si la détection globale estime que la ligne n'est français avec un score suffisant
        if (label != 'fr' and score >= CONFIDENCE_THRESHOLD) :
            print('kab',score)
            # Encadrer la ligne complète avec des balises <fr>...</fr>
            processed_lines[idx] = f"<unk>{lines[idx].strip()}</unk>\n"    
        if label == 'fr' and score <= CONFIDENCE_THRESHOLD:
            print("je suis ici")
            # Sinon, procéder à une détection token par token pour un traitement plus fin
            # Utilisation de wordpunct_tokenize pour découper la ligne en tokens simples
            tokens = wordpunct_tokenize(lines[idx])
            if not tokens:
                continue  # Passer la ligne si aucun token n'est trouvé
            # Traiter la détection de langue sur tous les tokens en une seule requête (batch)
            token_results = lang_detector(tokens, truncation=True)
            processed_tokens = []
            # Parcourir les tokens et leurs résultats respectifs
            for token, token_result in zip(tokens, token_results):
                token_label = token_result.get('label', '').replace('__label__', '')
                token_score = token_result.get('score', 0.0)
                # Si le token est détecté comme français avec un score suffisant, l'encadrer de balises
                if token_label == 'fr' and token_score >= CONFIDENCE_THRESHOLD:
                    processed_tokens.append(f"<frT>{token}</frT>")
            # Remplacer la ligne d'origine par la version traitée
            processed_lines[idx] = " ".join(processed_tokens) + "\n"
        else:
            print('kab',score)
            # Encadrer la ligne complète avec des balises <fr>...</fr>
            processed_lines[idx] = f"<unk>{lines[idx].strip()}</unk>\n"  

    # Écriture du contenu traité dans le fichier de sortie
    with open(output_filepath, "w", encoding="utf-8") as outfile:
        outfile.write("".join(processed_lines))
    
    logging.info(f"Fichier traité et sauvegardé dans : {output_filepath}")

def main():
    """
    Point d'entrée principal pour le traitement des fichiers.
    
    1. Définit les répertoires d'entrée et de sortie.
    2. Liste les fichiers Markdown à traiter.
    3. Traite chaque fichier en appelant la fonction process_file.
    """
    # Définir les chemins des répertoires source et destination (à adapter selon ton organisation)
    input_dir = "../data/pdfs_etat_2_separation/lot1/a_revoir"
    output_dir = "../data/pdfs_etat_3_tagged/lot1/a_revoir"
    
    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Lister tous les fichiers avec l'extension .md dans le répertoire d'entrée
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    logging.info(f"Nombre de fichiers à traiter : {len(md_files)}")

    # Traitement de chaque fichier en affichant une barre de progression
    for md_file in tqdm(md_files, desc="Traitement des fichiers"):
        input_filepath = os.path.join(input_dir, md_file)
        output_filepath = os.path.join(output_dir, md_file)
        process_file(input_filepath, output_filepath)

    logging.info("Traitement complet de tous les fichiers.")

# Point d'entrée principal du script. Exécute la fonction main() si le script est lancé directement.
if __name__ == "__main__":
    main()
