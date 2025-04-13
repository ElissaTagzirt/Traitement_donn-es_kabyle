#!/usr/bin/env python3
import os

# IMPORTANT : Assure-toi que ta clé API LlamaCloud est définie dans ton environnement.
# Par exemple, sous Linux/Mac, dans ton shell :
# export LLAMA_CLOUD_API_KEY='llx-123456789abcdef'
# Ou tu peux la définir directement ici (moins recommandé) :
os.environ["LLAMA_CLOUD_API_KEY"] = "llx-Xm5BMXFRBAHbpJrjlg3ojND7U8gQn5MIlP1WtVZbYcozusnf"

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
    
    Le paramètre 'extra_info' contient au moins le nom du fichier, nécessaire pour 
    que LlamaParse traite correctement le document.
    """
    # Extra info attendu par LlamaParse (ici, le nom du fichier)
    extra_info = {"file_name": os.path.basename(pdf_path)}
    
    # Ouvre le PDF en mode binaire
    with open(pdf_path, "rb") as f:
        # Initialise LlamaParse en mode "markdown"
        parser = LlamaParse(result_type="markdown")
        # Charge et parse le PDF ; load_data accepte un objet fichier et un extra_info
        documents = parser.load_data(f, extra_info=extra_info)
    
    # Écrit le contenu extrait dans le fichier Markdown de sortie
    with open(output_md, "w", encoding="utf-8") as out_file:
        for doc in documents:
            out_file.write(doc.text + "\n")
    
    print(f"Traitement du PDF {pdf_path} terminé. Résultat sauvegardé dans {output_md}")


def main():
    # Répertoires d'entrée et de sortie à adapter selon ton organisation
    PDF_INPUT_DIR = "."
    MD_OUTPUT_DIR = "."
    
    if not os.path.exists(MD_OUTPUT_DIR):
        os.makedirs(MD_OUTPUT_DIR)
    
    # Liste tous les fichiers PDF du dossier d'entrée
    pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.lower().endswith(".pdf")]
    
    # Traite les fichiers un par un (sans multiprocessing)
    for pdf_name in pdf_files:
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_name)
        base_name = os.path.splitext(pdf_name)[0]
        output_md = os.path.join(MD_OUTPUT_DIR, base_name + ".md")
        process_pdf(pdf_path, output_md)
    
    print("Traitement terminé pour tous les fichiers PDF.")


if __name__ == "__main__":
    main()
