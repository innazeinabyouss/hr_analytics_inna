import pandas as pd


def charger_donnees(chemin):
    """Lit le fichier CSV et renvoie le tableau."""
    df = pd.read_csv(chemin)
    return df