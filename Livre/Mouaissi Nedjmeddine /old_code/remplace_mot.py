import re

def replace_words_in_file(input_path, output_path):
    """
    Parcourt le fichier spécifié et remplace :
      - "kab" par "Tamaziɣt"
      - "fr" par "Tafransist"
    Les remplacements se font sur des mots entiers, sans tenir compte de la casse.
    """
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    replaced_lines = []
    for line in lines:
        # Remplacer le mot "kab" par "Tamaziɣt"
        #line = re.sub(r'\bkab\b', 'Tamaziɣt', line, flags=re.IGNORECASE)
        line = re.sub(r'\btexte\s*fr', 'Aḍris afransis', line, flags=re.IGNORECASE)
        line = re.sub(r'\btexte\s*kab', 'Aḍris tamaziɣt', line, flags=re.IGNORECASE)
        # Remplacer le mot "fr" par "Tafransist"
        #line = re.sub(r'\bfr\b', 'Tafransist', line, flags=re.IGNORECASE)
        replaced_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(replaced_lines)

def main():
    input_file = "./Markdown_tagged_roberta2/without_tables/beaucoup_de_francais/clean/clean_donne_81_Mas. Amz. 728.md"    # Remplacez par le chemin de votre fichier source
    output_file = "./Markdown_tagged_roberta2/without_tables/beaucoup_de_francais/clean/clean_waggi_donne_81_Mas. Amz. 728.md"  # Remplacez par le chemin souhaité pour le fichier modifié
    replace_words_in_file(input_file, output_file)
    print(f"Le fichier modifié a été enregistré dans : {output_file}")

if __name__ == '__main__':
    main()
