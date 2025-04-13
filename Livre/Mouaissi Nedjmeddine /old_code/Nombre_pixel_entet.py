import cv2
import numpy as np
from pdf2image import convert_from_path

# Chemin vers le fichier PDF
pdf_path = './PDFs/test/F7/fichier_7.pdf'

# Conversion de la première page du PDF en image
# Vous pouvez ajuster le dpi pour améliorer la résolution
pages = convert_from_path(pdf_path, dpi=300)
if not pages:
    print("Erreur : aucune page trouvée dans le PDF.")
    exit()

# Sélection de la première page
pil_image = pages[0]

# Conversion de l'image PIL en tableau NumPy pour OpenCV
# pdf2image fournit une image en mode RGB, il faut convertir en BGR pour OpenCV
image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

# Conversion en niveaux de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

height, width = gray.shape
bar_y = None

# Seuil pour détecter la barre : 
# ici, une moyenne inférieure à 250 (sur 255) indique un changement notable (la barre)
threshold = 250

# Parcours de chaque ligne de l'image depuis le haut
for y in range(height):
    # Calcul de la moyenne des intensités de la ligne y
    row_mean = np.mean(gray[y, :])
    # Si la ligne n'est pas presque entièrement blanche, on considère qu'il s'agit de la barre
    if row_mean < threshold:
        bar_y = y
        break

if bar_y is not None:
    print(f"Distance du haut de l'image à la barre : {bar_y} pixels")
else:
    print("Aucune barre détectée dans l'image.")
