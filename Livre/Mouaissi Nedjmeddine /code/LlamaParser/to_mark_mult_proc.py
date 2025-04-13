#!/usr/bin/env python3
import os
from multiprocessing import Pool

# IMPORTANT : Assure-toi que ta clé API LlamaCloud est définie dans ton environnement.
# Par exemple, sous Linux/Mac, dans ton shell :
# export LLAMA_CLOUD_API_KEY='llx-123456789abcdef'
# Ou tu peux la définir directement ici (moins recommandé) :
# os.environ["LLAMA_CLOUD_API_KEY"] = "llx-123456789abcdef"

os.environ["LLAMA_CLOUD_API_KEY"] = "llx-dpuWWf8ngZum2pyVrG7UFqAhRZ0JeSJMsuruEOkop2LU0Zr2"
try:
    from llama_parse import LlamaParse
except ImportError:
    raise ImportError(
        "La librairie llama-parse n'est pas installée. "
        "Installe-la via : pip install llama-parse"
    )


def process_pdf(pdf_path, output_md):
    """
    Lit le PDF à l'aide de LlamaParse et enregistre le contenu extrait au format Markdown.
    
    Le paramètre 'extra_info' contient au moins le nom de fichier,
    nécessaire pour que LlamaParse traite correctement le document.
    """
    # Extra info attendu par LlamaParse (ici, le nom du fichier)
    extra_info = {"file_name": os.path.basename(pdf_path)}
    
    # Ouvre le PDF en mode binaire
    with open(pdf_path, "rb") as f:
        # Initialise LlamaParse en mode "markdown"
        # Tu peux ajouter d'autres paramètres (par exemple, user_prompt, target_pages, bbox_top, etc.)
        parser = LlamaParse(result_type="markdown")
        # Charge et parse le PDF ; load_data accepte un objet fichier et un extra_info
        documents = parser.load_data(f, extra_info=extra_info)
    
    # Écrit le contenu extrait dans le fichier Markdown de sortie
    with open(output_md, "w", encoding="utf-8") as out_file:
        for doc in documents:
            # Chaque doc possède une propriété "text" qui contient le markdown généré
            out_file.write(doc.text + "\n")
    
    print(f"Traitement du PDF {pdf_path} terminé. Résultat sauvegardé dans {output_md}")


def process_pdf_worker(args):
    pdf_path, output_md = args
    process_pdf(pdf_path, output_md)


def main():
    # Répertoires d'entrée et sortie (à adapter selon ton organisation)
    PDF_INPUT_DIR = "../../data/pdfs_etat_0/text_selectable/traite/lot3"
    MD_OUTPUT_DIR = "../data/pdfs_etat_1_markdownllm/text_selectable/traite_v2/lot3"
    
    if not os.path.exists(MD_OUTPUT_DIR):
        os.makedirs(MD_OUTPUT_DIR)
    
    # Liste tous les fichiers PDF du dossier d'entrée
    pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.lower().endswith(".pdf")]
    
    tasks = []
    for pdf_name in pdf_files:
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_name)
        base_name = os.path.splitext(pdf_name)[0]
        output_md = os.path.join(MD_OUTPUT_DIR, base_name + ".md")
        tasks.append((pdf_path, output_md))
    
    # Utilisation du multiprocessing pour traiter plusieurs PDF en parallèle
    n_workers = 4  # Ajuste en fonction de tes ressources
    print(f"Utilisation de {n_workers} cœurs pour le traitement des PDFs.")
    with Pool(n_workers) as pool:
        pool.map(process_pdf_worker, tasks)
    
    print("Traitement terminé pour tous les fichiers PDF.")


if __name__ == "__main__":
    main()
