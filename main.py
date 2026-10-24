from src.config import CHEMIN_DONNEES, COLONNES_TEXTE, COLONNES_GRAPHIQUES
from src.load_data import charger_donnees
from src.explore import controle_qualite
from src.analyse import taux_depart, comparer_chiffres
from src.graphiques import graphique_taux

df = charger_donnees(CHEMIN_DONNEES)

controle_qualite(df)

for col in COLONNES_TEXTE:
    print("\n=====", col, "=====")
    print(taux_depart(df, col))

print("\n===== Médianes chiffrées =====")
print(comparer_chiffres(df))

for col in COLONNES_GRAPHIQUES:
    graphique_taux(df, col)

print("\n===== Modèle de prédiction =====")
try:
    from src.modele import comparer_modeles
    comparer_modeles(df)
except ImportError as erreur:
    print("Modèle non lancé : scikit-learn ne se charge pas sur cet ordinateur.")
    print("Détail :", erreur)