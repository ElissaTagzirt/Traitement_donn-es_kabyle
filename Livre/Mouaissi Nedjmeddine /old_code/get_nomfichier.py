
import os

def extract_identifiers(source_dir, output_file):
    """
    Parcourt tous les fichiers PDF dans source_dir,
    extrait le numéro identifiant (la partie avant le premier '_')
    et les écrit dans output_file (un identifiant par ligne).
    """
    identifiers = set()  # Utilisation d'un ensemble pour éviter les doublons
    
    # Parcours des fichiers du répertoire source
    for filename in os.listdir(source_dir):
        chemin_complet = os.path.join(source_dir, filename)
        if os.path.isfile(chemin_complet) and filename.lower().endswith('.md'):
            # Extraction du numéro identifiant
            parts = filename.split('_')
            if parts:
                
                identifier = parts[0]
                identifiers.add(identifier)
    
    # Écriture des identifiants dans le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        for ident in sorted(identifiers, key=lambda x: int(x) if x.isdigit() else x):
            f.write(ident + '\n')

def main():
    source_dir = "./Markdown_tagged_roberta2/without_tables/moyennement_de_francais/pure"
      # Répertoire contenant les fichiers PDF
    output_file = 'identifiants.txt'
    
    extract_identifiers(source_dir, output_file)
    print(f"Les identifiants ont été extraits et sauvegardés dans '{output_file}'.")

if __name__ == '__main__':
    main()
