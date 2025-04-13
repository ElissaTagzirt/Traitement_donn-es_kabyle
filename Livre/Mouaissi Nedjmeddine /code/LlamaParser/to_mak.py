#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from llama_cloud_services import LlamaParse

def main():
    # Instanciation du parseur avec les paramètres adaptés
    parser = LlamaParse(
        api_key="llx-Xm5BMXFRBAHbpJrjlg3ojND7U8gQn5MIlP1WtVZbYcozusnf",  # Remplace par ton token d'authentification valide
        verbose=True,
    )
    
    # Chargement du fichier PDF
    documents = parser.load_data("./data/ussan-di-tmurt.pdf")

    # Extraction du texte de tous les documents (pages)
    full_text = ""
    for doc in documents:
        full_text += doc.text + "\n\n"

    # Sauvegarde dans un fichier Markdown
    output_path = "./output/ussan-di-tmurt.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Le contenu a été extrait et sauvegardé dans : {output_path}")

if __name__ == "__main__":
    main()
