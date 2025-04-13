def clean_md_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Garde uniquement les lignes qui commencent par un tiret "-"
    filtered_lines = [line for line in lines if line.lstrip().startswith('-')]

    # Écrit le résultat dans le fichier de sortie
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(filtered_lines)

# Exemple d'utilisation
clean_md_file('../Inzan – 231 Proverbes Berbères de Kabylie – O. Ould-Braham – PDF 46 pages.pdf.md', 'Inzan – 231 Proverbes Berbères de Kabylie – O. Ould-Braham – PDF 46 pages_corrige.md')
