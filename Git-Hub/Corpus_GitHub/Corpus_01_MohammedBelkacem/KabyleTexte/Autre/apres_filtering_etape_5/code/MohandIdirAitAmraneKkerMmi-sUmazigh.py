#!/usr/bin/env python3
import sys
import re

def modifier_fichier():
    # Noms de fichiers en dur
    chemin_entree = "Mouloud Feraoun Moussa Ould Taleb_modifie.pdf.md"
    chemin_sortie = "sortie2.md"
    
    try:
        # Lecture du contenu du fichier d'entrée
        with open(chemin_entree, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        
        # Remplacer "Mǧulǧud" par "Mulud"
        contenu_modifie = contenu.replace("Mǧulǧud", "Mulud")
        
        # Remplacer "Feraǧun" par "Feraɛun"
        contenu_modifie = contenu_modifie.replace("Feraǧun", "Feraɛun")
        # Supprimer les espaces supplémentaires avant "ɣer"
        contenu_modifie = re.sub(r'\s+(?=ɣer)', ' ', contenu_modifie)

        contenu_modifie = contenu.replace("ñ", "t")
        contenu_modifie = contenu.replace("ñ", "t")


        # Sauvegarde du contenu modifié dans le fichier de sortie
        with open(chemin_sortie, 'w', encoding='utf-8') as fichier:
            fichier.write(contenu_modifie)
        
        print(f"Le fichier modifié a été sauvegardé sous '{chemin_sortie}'.")
    
    except Exception as e:
        print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    modifier_fichier()
