#!/usr/bin/env python3
import os
import re
import pdfplumber
import ray

# ====================================
# Définitions des Regex et nettoyage
# ====================================
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

# ====================================
# Regroupement des mots en lignes
# ====================================
def group_words_into_lines(words_sorted, y_threshold=10):
    """
    Regroupe une liste de mots (triés par leur position verticale) en lignes.
    Si la différence entre le 'top' d'un mot et la valeur de référence est <= y_threshold,
    il est considéré comme appartenant à la même ligne.
    Retourne une liste de tuples (avg_y, ligne_texte).
    """
    lines = []
    current_line = []
    current_y = None
    for w in words_sorted:
        text = w["text"]
        top = w["top"]
        if current_y is None:
            current_y = top
            current_line = [text]
        else:
            if abs(top - current_y) <= y_threshold:
                current_line.append(text)
            else:
                line_str = " ".join(current_line).strip()
                lines.append((current_y, line_str))
                current_line = [text]
                current_y = top
    if current_line:
        line_str = " ".join(current_line).strip()
        lines.append((current_y, line_str))
    return lines

# ====================================
# Traitement d'une page (texte uniquement)
# ====================================
def process_page_text(page, header_cutoff=100, col_split_x=None):
    """
    Traite une page en séparant la zone d'en-tête (0 à header_cutoff)
    de la zone principale (header_cutoff à la fin de la page).
    Extraction du texte avec pdfplumber.
    Si col_split_x est défini, on reconstruit le texte principal à partir des mots extraits.
    
    Retourne deux listes :
      - header_lines_clean : lignes extraites de la zone d'en-tête.
      - main_lines_clean   : lignes extraites du corps de la page.
    """
    header_bbox = (0, 0, page.width, header_cutoff)
    main_bbox = (0, header_cutoff, page.width, page.height)
    
    header_text = page.within_bbox(header_bbox).extract_text() or ""
    main_text = page.within_bbox(main_bbox).extract_text() or ""
    
    header_lines = [clean_line(line) for line in header_text.split("\n") if line.strip()]
    main_lines = [clean_line(line) for line in main_text.split("\n") if line.strip()]
    
    # Si le document est en colonnes, reconstruire le texte principal via extract_words()
    if col_split_x is not None:
        main_words = page.within_bbox(main_bbox).extract_words() or []
        col1_words = [w for w in main_words if w["x0"] < col_split_x]
        col2_words = [w for w in main_words if w["x0"] >= col_split_x]
        col1_words = sorted(col1_words, key=lambda w: (w["top"], w["x0"]))
        col2_words = sorted(col2_words, key=lambda w: (w["top"], w["x0"]))
        col1_lines_tuples = group_words_into_lines(col1_words, y_threshold=10)
        col2_lines_tuples = group_words_into_lines(col2_words, y_threshold=10)
        col1_lines = [ln for (_, ln) in col1_lines_tuples]
        col2_lines = [ln for (_, ln) in col2_lines_tuples]
        main_lines = col1_lines + col2_lines
    
    header_lines_clean = [line for line in header_lines if line]
    main_lines_clean = [line for line in main_lines if line]
    
    return header_lines_clean, main_lines_clean

# ====================================
# Traitement complet d'un PDF
# ====================================
def process_pdf(pdf_path, output_md, header_cutoff=100, col_split_x=None):
    """
    Parcourt toutes les pages d'un PDF, extrait le texte de l'en-tête et du corps,
    et écrit le tout dans un fichier Markdown.
    """
    with pdfplumber.open(pdf_path) as pdf, open(output_md, "w", encoding="utf-8") as md_file:
        num_pages = len(pdf.pages)
        md_file.write(f"# Extraction du PDF : {os.path.basename(pdf_path)}\n")
        md_file.write(f"(Total pages: {num_pages})\n\n")
        for i, page in enumerate(pdf.pages):
            md_file.write(f"\n## Page {i+1}\n\n")
            header_texts, main_texts = process_page_text(page, header_cutoff=header_cutoff, col_split_x=col_split_x)
            if header_texts:
                md_file.write("### HEADER\n")
                for h in header_texts:
                    md_file.write(h + "\n")
                md_file.write("\n")
            for line in main_texts:
                md_file.write(line + "\n")
            md_file.write("\n")
            
            # Extraction des tableaux (si besoin)
            tables = page.extract_tables()
            if tables:
                for t_i, table in enumerate(tables):
                    md_file.write(f"\n**TABLE {t_i+1}**:\n")
                    for row in table:
                        row_text = " | ".join(cell if cell else "" for cell in row)
                        md_file.write(row_text + "\n")
                md_file.write("\n")

@ray.remote(num_gpus=1)
def process_pdf_worker_remote(pdf_path, output_md, header_cutoff, col_split_x):
    """
    Fonction worker distante pour le traitement d'un PDF.
    Chaque tâche est assignée à un GPU grâce à Ray.
    """
    print(f"Processing {pdf_path} => {output_md}")
    process_pdf(pdf_path, output_md, header_cutoff, col_split_x)

def main():
    PDF_INPUT_DIR = "./PDFs/non_imp/with_tables"  # Répertoire contenant les PDF
    MD_OUTPUT_DIR = "./Markdown_non/with_tables"   # Répertoire de sortie pour les fichiers Markdown
    if not os.path.exists(MD_OUTPUT_DIR):
        os.makedirs(MD_OUTPUT_DIR)
    pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.lower().endswith(".pdf")]
    
    tasks = []
    header_cutoff = 100
    col_split_x = None
    for pdf_name in pdf_files:
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_name)
        base_name = os.path.splitext(pdf_name)[0]
        output_md = os.path.join(MD_OUTPUT_DIR, base_name + ".md")
        tasks.append(process_pdf_worker_remote.remote(pdf_path, output_md, header_cutoff, col_split_x))
    
    # Lancement et attente de toutes les tâches sur GPU
    ray.get(tasks)

if __name__ == "__main__":
    # Initialisation de Ray pour gérer la distribution sur GPU
    ray.init()
    main()
