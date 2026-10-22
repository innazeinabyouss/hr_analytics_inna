import os
import matplotlib.pyplot as plt
from src.analyse import taux_depart


def graphique_taux(df, colonne, dossier="outputs"):
    """Dessine le % de départ pour chaque valeur d'une colonne, et l'enregistre en image."""
    os.makedirs(dossier, exist_ok=True)

    taux = taux_depart(df, colonne)["mean"].sort_values() * 100
    taux.index = taux.index.fillna("Vide")
    taux.plot(kind="barh", title=f"% qui veulent changer de job, par {colonne}")
    plt.xlabel("% de départ")
    plt.tight_layout()

    chemin = f"{dossier}/taux_{colonne}.png"
    plt.savefig(chemin)
    plt.close()
    print("Graphique enregistré :", chemin)