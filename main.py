from src.load_data import charger_donnees
from src.explore import controle_qualite
from src.analyse import taux_depart, comparer_chiffres
from src.graphiques import graphique_taux
from src.modele import entrainer_modele

COLONNES = [
    "gender", "relevent_experience", "enrolled_university",
    "education_level", "major_discipline", "experience",
    "company_size", "company_type", "last_new_job",
]

df = charger_donnees("data/aug_train.csv")

controle_qualite(df)

for col in COLONNES:
    print("\n=====", col, "=====")
    print(taux_depart(df, col))

print("\n===== Médianes chiffrées =====")
print(comparer_chiffres(df))

for col in ["education_level", "experience", "enrolled_university", "company_size"]:
    graphique_taux(df, col)

print("\n===== Modèle de prédiction =====")
modele = entrainer_modele(df)