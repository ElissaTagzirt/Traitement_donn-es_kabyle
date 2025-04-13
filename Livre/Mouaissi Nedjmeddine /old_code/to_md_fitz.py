#!/usr/bin/env python3
import os
import re
import fitz  # PyMuPDF
import camelot

# ===========================================
# Définitions des Regex et fonction clean_line
# ===========================================
CHAPITRE_PATTERN = re.compile(r'(?i)^\s*chapitre\s*\S*')
BIBLIO_REF_PATTERN = re.compile(r'^\s*[0-9¹²³⁴-⁹]+\s+.*(éd|ed\.|p\.?\s*\d+)', re.IGNORECASE)

def clean_line(line):
    """
    Nettoie une ligne en retirant les espaces superflus.
    En fonction du contenu, enveloppe la ligne dans <header> ou <footer>.
    """
    line = line.strip()
    if not line:
        return ""
    if CHAPITRE_PATTERN.search(line):
        return f"<header>{line}</header>"
    elif BIBLIO_REF_PATTERN.search(line):
        return f"<footer>{line}</footer>"
    return line

# ===========================================
# Extraction du texte avec PyMuPDF (cropping)
# ===========================================
def extract_text_from_page(page, header_cutoff=100):
    """
    Sépare la page en deux zones :
      - Zone d’en‑tête : du haut de la page jusqu'à header_cutoff (en pixels)
      - Zone principale : de header_cutoff à la fin de la page
    Extrait le texte de chaque zone à l’aide de get_textbox().
    Applique clean_line() sur chaque ligne.
    Retourne deux listes de chaînes (en-tête et corps).
    """
    # Définition des rectangles
    header_rect = fitz.Rect(0, 0, page.rect.width, header_cutoff)
    main_rect = fitz.Rect(0, header_cutoff, page.rect.width, page.rect.height)
    
    # Extraction du texte dans chaque zone
    header_text = page.get_textbox(header_rect)
    main_text = page.get_textbox(main_rect)
    
    # Découper en lignes et nettoyer
    header_lines = [clean_line(line) for line in header_text.splitlines() if line.strip()]
    main_lines = [clean_line(line) for line in main_text.splitlines() if line.strip()]
    
    return header_lines, main_lines

# ===========================================
# Traitement complet d'un PDF (texte et tableaux)
# ===========================================
def process_pdf(pdf_path, output_md, header_cutoff=100):
    """
    Traite un PDF en utilisant PyMuPDF pour extraire le texte (séparation en en‑tête et corps)
    et Camelot pour extraire les tableaux.
    Le résultat est écrit dans un fichier Markdown.
    """
    # Extraction du texte avec PyMuPDF
    doc = fitz.open(pdf_path)
    with open(output_md, "w", encoding="utf-8") as md_file:
        md_file.write(f"# Extraction du PDF : {os.path.basename(pdf_path)}\n")
        md_file.write(f"(Total pages: {doc.page_count})\n\n")
        for i in range(doc.page_count):
            page = doc[i]
            md_file.write(f"\n## Page {i+1}\n\n")
            header_lines, main_lines = extract_text_from_page(page, header_cutoff=header_cutoff)
            if header_lines:
                md_file.write("### HEADER\n")
                for line in header_lines:
                    md_file.write(line + "\n")
                md_file.write("\n")
            for line in main_lines:
                md_file.write(line + "\n")
            md_file.write("\n")
    doc.close()
    
    # Extraction des tableaux avec Camelot (Camelot lit directement le PDF)
  

# ===========================================
# Fonction main
# ===========================================
def main():
    PDF_INPUT_DIR = "./PDFs/test/F14"         # Répertoire contenant vos PDF
    MD_OUTPUT_DIR = "./PDFs/test/extracted/14" # Répertoire de sortie pour les fichiers .md
    if not os.path.exists(MD_OUTPUT_DIR):
        os.makedirs(MD_OUTPUT_DIR)
    pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.lower().endswith(".pdf")]
    for pdf_name in pdf_files:
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_name)
        base_name = os.path.splitext(pdf_name)[0]
        output_md = os.path.join(MD_OUTPUT_DIR, base_name + ".md")
        print(f"Processing {pdf_path} => {output_md}")
        process_pdf(pdf_path, output_md, header_cutoff=60)

if __name__ == "__main__":
    main()
