#!/usr/bin/env python3
import os
import pdfplumber
import shutil

def has_tables(pdf_path):
    """
    Vérifie si un PDF contient au moins un tableau.
    Retourne True si un tableau est trouvé sur l'une des pages, sinon False.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                # Si au moins un tableau non vide est trouvé, retourne True.
                if tables and any(len(table) > 2 for table in tables):
                    return True
    except Exception as e:
        print(f"Erreur lors de l'ouverture de {pdf_path} : {e}")
    return False

def separate_pdfs(input_dir, with_tables_dir, without_tables_dir):
    """
    Parcourt tous les fichiers PDF du répertoire input_dir.
    Déplace les fichiers contenant des tableaux dans with_tables_dir
    et ceux sans tableaux dans without_tables_dir.
    """
    os.makedirs(with_tables_dir, exist_ok=True)
    os.makedirs(without_tables_dir, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        print(f"Traitement de {pdf_file}...")
        if has_tables(pdf_path):
            print(f"  -> Contient des tableaux. Déplacement vers {with_tables_dir}")
            shutil.move(pdf_path, os.path.join(with_tables_dir, pdf_file))
        else:
            print(f"  -> Ne contient pas de tableaux. Déplacement vers {without_tables_dir}")
            shutil.move(pdf_path, os.path.join(without_tables_dir, pdf_file))

def main():
    # Répertoire source contenant les fichiers PDF à traiter
    PDF_INPUT_DIR = "./PDFs/with_tables"
    
    # Répertoires de sortie pour les PDF avec et sans tableaux
    WITH_TABLES_DIR = "./PDFs/with_tables/with_tables"
    WITHOUT_TABLES_DIR = "./PDFs/with_tables/without_tables"
    
    separate_pdfs(PDF_INPUT_DIR, WITH_TABLES_DIR, WITHOUT_TABLES_DIR)
    print("Séparation terminée.")

if __name__ == "__main__":
    main()
