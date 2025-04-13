def nettoyer_markdown(input_path: str, output_path: str):
    lignes_filtrees = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for ligne in f:
            ligne = ligne.strip()

            # Supprimer toute ligne contenant exactement "Haǧira U Bacir"
            if ligne == "Timenna n Saɛid Iɛemrac":
                continue

            # Supprimer le mot "Amezgun" s'il apparaît dans la ligne
            #ligne = ligne.replace("Amezgun", "")

            lignes_filtrees.append(ligne + "\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lignes_filtrees)

    print(f"✔️ Fichier Markdown nettoyé sauvegardé dans : {output_path}")

# Exemple d'utilisation
input_md = "038-Said Iamrache.pdf.md"
output_md = "38-Said Iamrache.pdf.md"
nettoyer_markdown(input_path=input_md, output_path=output_md)
