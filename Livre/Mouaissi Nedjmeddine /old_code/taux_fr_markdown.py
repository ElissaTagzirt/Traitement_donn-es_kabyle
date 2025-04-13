import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import matplotlib.ticker as mtick
import matplotlib.ticker as ticker

def compute_french_ratio(filepath):
    """
    Lit le fichier Markdown, compte le nombre total de mots et ceux situés
    entre <french>...</french>, puis calcule le ratio de contenu français.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    total_words = len(re.findall(r'\w+', text))
    french_segments = re.findall(r'<fr>(.*?)</fr>', text, flags=re.DOTALL)
    french_words = sum(len(re.findall(r'\w+', segment)) for segment in french_segments)
    ratio = french_words / total_words if total_words else 0
    return ratio

def traverse_directory(directory):
    """
    Parcourt le répertoire et ses sous-dossiers pour trouver les fichiers Markdown (.md),
    calcule le ratio de contenu français pour chacun et retourne une liste de ratios et 
    la liste correspondante des chemins de fichiers.
    """
    ratios = []
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.md'):
                filepath = os.path.join(root, file)
                ratio = compute_french_ratio(filepath)
                ratios.append(ratio)
                file_names.append(filepath)
    return ratios, file_names

def create_plots_with_quartiles(ratios):
    """
    Calcule et affiche les statistiques globales (moyenne, médiane, premier quartile (Q1),
    troisième quartile (Q3), écart-type, min, max) des ratios de contenu français,
    puis crée un histogramme avec la courbe de densité.
    L'axe des x est affiché en pourcentage avec des pas de 5%.
    Des lignes verticales sont tracées pour la médiane, Q1 et Q3.
    Le graphique est enregistré dans "histogram_french_ratio_with_quartiles.png".
    """
    mean_ratio = np.mean(ratios)
    median_ratio = np.median(ratios)
    q1 = np.percentile(ratios, 25)
    q3 = np.percentile(ratios, 75)
    std_ratio = np.std(ratios)
    min_ratio = np.min(ratios)
    max_ratio = np.max(ratios)
    
    # Affichage des statistiques
    print("Statistiques globales du ratio de contenu français :")
    print(f"  Moyenne           : {mean_ratio:.2%}")
    print(f"  Médiane (Q2)      : {median_ratio:.2%}")
    print(f"  1er Quartile (Q1) : {q1:.2%}")
    print(f"  3e Quartile (Q3)  : {q3:.2%}")
    print(f"  Écart-type        : {std_ratio:.2%}")
    print(f"  Minimum           : {min_ratio:.2%}")
    print(f"  Maximum           : {max_ratio:.2%}")
    
    # Création de l'histogramme avec la densité
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bins avec pas de 5% (de 0 à 1 en 21 intervalles)
    bins = np.linspace(0, 1, 21)
    ax.hist(ratios, bins=bins, density=True, alpha=0.6, edgecolor='black', label='Histogramme')
    
    # Ligne verticale pour la moyenne
    ax.axvline(mean_ratio, color='red', linestyle='--', linewidth=2, label=f'Moyenne ({mean_ratio:.2%})')
    
    # Lignes verticales pour Q1, la médiane et Q3
    ax.axvline(q1, color='green', linestyle='-.', linewidth=2, label=f'Q1 (25%) ({q1:.2%})')
    ax.axvline(median_ratio, color='orange', linestyle='-.', linewidth=2, label=f'Médiane (Q2) ({median_ratio:.2%})')
    ax.axvline(q3, color='purple', linestyle='-.', linewidth=2, label=f'Q3 (75%) ({q3:.2%})')
    
    # Calcul et tracé de la courbe de densité
    if len(ratios) > 1:
        density = gaussian_kde(ratios)
        xs = np.linspace(0, 1, 200)
        ax.plot(xs, density(xs), color='blue', label='Densité estimée')
    
    ax.set_title("Distribution du ratio de contenu français")
    ax.set_xlabel("Ratio de contenu français (%)")
    ax.set_ylabel("Densité")
    
    # Formatage de l'axe des x en pourcentage avec des pas de 5%
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.05))
    
    ax.legend()
    plt.tight_layout()
    
    output_image = "histogram_french_ratio_with_quartiles_roberta_without_tables_V1.png"
    plt.savefig(output_image)
    print(f"L'image a été enregistrée sous : {output_image}")
    plt.show()

def main():
    directory = "./Markdown_tagged_roberta2/without_tables"
    ratios, file_names = traverse_directory(directory)
    
    print("Ratios de contenu français par fichier :")
    for file, ratio in zip(file_names, ratios):
        print(f"{file}: {ratio:.2%}")
    
    create_plots_with_quartiles(ratios)

if __name__ == '__main__':
    main()
