from src.config import COLONNES_CHIFFRES

def taux_depart(df, colonne):
    """% de personnes qui veulent partir, pour chaque valeur d'une colonne."""
    resultat = df.groupby(colonne, dropna=False)["target"].agg(["count", "mean"])
    return resultat.round(3).sort_values("mean", ascending=False)


def comparer_chiffres(df):
    """Compare les médianes des colonnes chiffrées entre ceux qui restent et ceux qui partent."""
    return df.groupby("target")[COLONNES_CHIFFRES].median()