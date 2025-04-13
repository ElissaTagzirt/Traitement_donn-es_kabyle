#!/usr/bin/env python3
import os
import re
import pdfplumber

PDF_INPUT_DIR = "./PDFs/test"
MD_OUTPUT_DIR = "./PDFs/test/extracted_col"

# Vos patterns
CHAPITRE_PATTERN = re.compile(r'(?i)^\s*chapitre\s*\S*')
BIBLIO_REF_PATTERN = re.compile(r'^\s*[0-9¹²³⁴-⁹]+\s+.*(éd|ed\.|p\.?\s*\d+)', re.IGNORECASE)

def clean_line(line):
    """
    Applique vos règles de nettoyage :
    - balises <header> si "Chapitre ..."
    - balises <footer> si ref biblio
    """
    line = line.strip()
    if not line:
        return ""
    if CHAPITRE_PATTERN.search(line):
        return f"<header>{line}</header>"
    elif BIBLIO_REF_PATTERN.search(line):
        return f"<footer>{line}</footer>"
    return line

def extract_pdf_text_and_tables(pdf_path):
    """
    Ouvre un PDF avec pdfplumber et renvoie la liste
    de toutes les lignes (texte brut + contenu des tableaux).
    """
    all_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            # 1) Extraire texte classique
            text = page.extract_text() or ""
            for line in text.split("\n"):
                if line.strip():
                    all_lines.append(line)

            # 2) Extraire contenu de tableaux
            tables = page.extract_tables()
            for table in tables:
                # table = liste de lignes, chaque ligne = liste de cellules
                for row in table:
                    # row = ["cell1", "cell2", ...]
                    for cell in row:
                        if cell:  # éviter "None"
                            all_lines.append(cell)
    return all_lines

def process_single_pdf(pdf_path, output_dir):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = os.path.join(output_dir, base_name + ".md")

    print(f"Extraction du PDF : {pdf_path}")

    # Récupérer tout le texte, y compris dans les tableaux
    raw_lines = extract_pdf_text_and_tables(pdf_path)

    # Nettoyer chaque ligne
    cleaned = []
    for line in raw_lines:
        c_line = clean_line(line)
        if c_line.strip():
            cleaned.append(c_line)

    # Écrire dans un fichier .md (ou .txt)
    with open(md_path, "w", encoding="utf-8") as md_file:
        for line in cleaned:
            md_file.write(line + "\n")

    print(f"Fichier créé : {md_path}")

def main():
    if not os.path.exists(MD_OUTPUT_DIR):
        os.makedirs(MD_OUTPUT_DIR)

    # Parcourir tous les PDF du dossier
    pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.lower().endswith(".pdf")]
    for pdf_name in pdf_files:
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_name)
        process_single_pdf(pdf_path, MD_OUTPUT_DIR)

if __name__ == "__main__":
    main()


