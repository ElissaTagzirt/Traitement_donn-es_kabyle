#!/usr/bin/env python3
import sys
import re

def modifier_fichier():
    # Noms de fichiers en dur
    chemin_entree = "sortie2.md"
    chemin_sortie = "sortie3.md"
    
    try:
        # Lecture du contenu du fichier d'entrée
        with open(chemin_entree, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        
        # Enchaîner les remplacements sur le contenu déjà modifié
        contenu_modifie = contenu.replace("Mǧulǧud", "Mulud")
        contenu_modifie = contenu_modifie.replace("Feraǧun", "Feraɛun")
        contenu_modifie = re.sub(r'\s+(?=ɣer)', ' ', contenu_modifie)
        contenu_modifie = contenu_modifie.replace("ñ", "t")
        contenu_modifie = contenu_modifie.replace("ú", "č")
        contenu_modifie = contenu_modifie.replace("á", "č")
        contenu_modifie = contenu_modifie.replace("Û", "ḥ")
        contenu_modifie = contenu_modifie.replace("µ", "ɛ")
        contenu_modifie = contenu_modifie.replace("Á", "č")
        # Sauvegarde du contenu modifié dans le fichier de sortie
        with open(chemin_sortie, 'w', encoding='utf-8') as fichier:
            fichier.write(contenu_modifie)
        
        print(f"Le fichier modifié a été sauvegardé sous '{chemin_sortie}'.")
    
    except Exception as e:
        print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    modifier_fichier()
