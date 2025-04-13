#!/usr/bin/env python3
import os
import re
import pdfplumber

# =========================
#  Définitions des Regex
# =========================
# Si une ligne commence par "chapitre", elle sera enveloppée dans une balise <header>
CHAPITRE_PATTERN = re.compile(r'(?i)^\s*chapitre\s*\S*')
# Si une ligne commence par des chiffres ou exposants suivis d’un texte typique de référence bibliographique,
# elle sera enveloppée dans une balise <footer>
BIBLIO_REF_PATTERN = re.compile(r'^\s*[0-9¹²³⁴-⁹]+\s+.*(éd|ed\.|p\.?\s*\d+)', re.IGNORECASE)

# Fonction de nettoyage appliquée à chaque ligne
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

# =========================
#  Extraction via cropping
# =========================
def process_page(page, header_cutoff, col_split_x=None):
    """
    Traite une page PDF en utilisant le découpage (cropping) pour séparer la zone d'en-tête
    de celle du texte principal.
    
    Paramètres :
      - header_cutoff : hauteur en pixels à partir du haut de la page considérée comme en-tête.
      - col_split_x : si défini (en pixels), le texte principal est séparé en deux colonnes (gauche et droite).
    
    Retourne :
      - header_lines_clean : liste des lignes extraites de la zone d'en-tête (nettoyées).
      - main_lines_clean   : liste des lignes extraites de la zone principale (nettoyées).
      - tables             : tableaux extraits par pdfplumber (si présents).
    """
    # Définition de la zone d'en-tête : du coin supérieur gauche (0,0) à (page.width, header_cutoff)
    header_bbox = (0, 0, page.width, header_cutoff)
    # Zone principale : du bas de l'en-tête jusqu'au bas de la page
    main_bbox = (0, header_cutoff, page.width, page.height)

    # Extraction du texte dans chaque zone
    header_text = page.within_bbox(header_bbox).extract_text() or ""
    main_text = page.within_bbox(main_bbox).extract_text() or ""

    # On sépare en lignes et on nettoie
    header_lines = [clean_line(line) for line in header_text.split("\n") if line.strip()]
    main_lines = [clean_line(line) for line in main_text.split("\n") if line.strip()]

    # Traitement des colonnes si col_split_x est défini
    if col_split_x is not None:
        main_words = page.within_bbox(main_bbox).extract_words()
        if main_words is None:
            main_words = []
        col1_words = [w for w in main_words if w["x0"] < col_split_x]
        col2_words = [w for w in main_words if w["x0"] >= col_split_x]
        col1_words = sorted(col1_words, key=lambda w: (w["top"], w["x0"]))
        col2_words = sorted(col2_words, key=lambda w: (w["top"], w["x0"]))
        col1_lines_tuples = group_words_into_lines(col1_words, y_threshold=5)
        col2_lines_tuples = group_words_into_lines(col2_words, y_threshold=5)
        col1_lines = [ln for (_, ln) in col1_lines_tuples]
        col2_lines = [ln for (_, ln) in col2_lines_tuples]
        main_lines = col1_lines + col2_lines

    # Extraction des tableaux
    tables = page.extract_tables()
    return header_lines, main_lines, tables

# =========================
#  Regroupement des mots en lignes (pour le cas colonne)
# =========================
def group_words_into_lines(words_sorted, y_threshold=5):
    """
    Regroupe une liste de mots triés par leur position verticale en lignes.
    Si la différence entre le 'top' d'un mot et la valeur de référence est inférieure ou égale à y_threshold,
    ils sont considérés comme appartenant à la même ligne.
    
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

# =========================
#  Traitement complet d'un PDF
# =========================
def process_pdf(pdf_path, output_md, header_cutoff, col_split_x=None):
    """
    Parcourt toutes les pages d'un PDF, extrait le texte de l'en-tête (zone supérieure)
    et le texte principal (zone restante), récupère aussi les tableaux, et écrit le tout dans un fichier Markdown.
    """
    with pdfplumber.open(pdf_path) as pdf, open(output_md, "w", encoding="utf-8") as md_file:
        num_pages = len(pdf.pages)
        md_file.write(f"# Extraction du PDF : {os.path.basename(pdf_path)}\n")
        md_file.write(f"(Total pages: {num_pages})\n\n")

        for i, page in enumerate(pdf.pages):
            md_file.write(f"\n## Page {i+1}\n\n")

            header_texts, main_texts, tables = process_page(page, header_cutoff=header_cutoff, col_split_x=col_split_x)

            # Écriture des en-têtes extraits
            if header_texts:
                md_file.write("### HEADER\n")
                for h in header_texts:
                    md_file.write(h + "\n")
                md_file.write("\n")

            # Écriture du texte principal
            for line in main_texts:
                md_file.write(line + "\n")
            md_file.write("\n")

            # Écriture des tableaux au format Markdown
            if tables:
                for t_i, table in enumerate(tables):
                    md_file.write(f"\n**TABLE {t_i+1}:**\n\n")
                    if table and len(table) > 0:
                        # Considérer la première ligne comme en-tête
                        header = table[0]
                        header_row = "| " + " | ".join(header) + " |"
                        separator = "| " + " | ".join(["---"] * len(header)) + " |"
                        md_file.write(header_row + "\n")
                        md_file.write(separator + "\n")
                        for row in table[1:]:
                            row_text = "| " + " | ".join(cell if cell else "" for cell in row) + " |"
                            md_file.write(row_text + "\n")
                    md_file.write("\n")

def main():
    PDF_INPUT_DIR = "./PDFs/test/F14"         # Répertoire contenant vos PDF
    MD_OUTPUT_DIR = "./PDFs/test/extracted/14"  # Répertoire de sortie pour les fichiers .md

    if not os.path.exists(MD_OUTPUT_DIR):
        os.makedirs(MD_OUTPUT_DIR)

    pdf_files = [f for f in os.listdir(PDF_INPUT_DIR) if f.lower().endswith(".pdf")]
    for pdf_name in pdf_files:
        pdf_path = os.path.join(PDF_INPUT_DIR, pdf_name)
        base_name = os.path.splitext(pdf_name)[0]
        output_md = os.path.join(MD_OUTPUT_DIR, base_name + ".md")

        print(f"Processing {pdf_path} => {output_md}")
        # Ajustez header_cutoff (ex: 60) et col_split_x (None ou une valeur) selon vos besoins.
        process_pdf(pdf_path, output_md, header_cutoff=60, col_split_x=None)

if __name__ == "__main__":
    main()
