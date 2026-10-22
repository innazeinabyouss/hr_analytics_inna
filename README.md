# HR Analytics – Qui veut changer de job ?

## Objectif
Comprendre quels profils de candidats veulent quitter l'entreprise après leur formation.
Enjeu : éviter de former des personnes qui partent, donc réduire les coûts de formation et de recrutement.

## Structure
```
data/        → données brutes (on ne les modifie jamais)
src/         → le code, rangé par tâche
  load_data.py   → charger les données
  explore.py     → contrôle qualité
  analyse.py     → taux de départ par groupe
  graphiques.py  → graphiques enregistrés en image
outputs/     → graphiques produits
main.py      → lance tout
```

## Lancer le projet
```
pip install -r requirements.txt
python main.py
```

## Résultats clés
- 25 % des candidats veulent partir (données déséquilibrées).
- Profil qui part le plus : peu d'expérience, en formation à temps plein, Graduate, ville peu développée.
- Les cases vides sont un signal : 40 % de départ quand `company_size` est vide (contre 25 % en moyenne).
- `training_hours` et `major_discipline` ont peu d'influence.