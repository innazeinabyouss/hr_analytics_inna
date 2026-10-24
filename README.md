# HR Analytics – Qui veut changer de job ?

## Objectif
Comprendre quels profils de candidats veulent quitter l'entreprise après leur formation.
Enjeu : éviter de former des personnes qui partent, donc réduire les coûts de formation et de recrutement.

## Structure
```
data/        → données brutes (on ne les modifie jamais)
src/         → le code, rangé par tâche
  config.py      → tous les réglages (chemin, colonnes)
  load_data.py   → charger les données
  explore.py     → contrôle qualité
  analyse.py     → taux de départ par groupe
  graphiques.py  → graphiques enregistrés en image
  modele.py      → modèle de prédiction (baseline)
outputs/     → graphiques produits
main.py      → lance tout

## Données
Télécharger `aug_train.csv` sur Kaggle :
https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists
Puis le placer dans le dossier `data/`.

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
- - Comparaison de 3 modèles, validation croisée sur 5 découpages :
  - Régression logistique (baseline) : AUC 0,782 (± 0,006)
  - Random Forest : AUC 0,801 (± 0,003), entraînement 2,9 s
  - Gradient Boosting : AUC 0,801 (± 0,003), entraînement 0,5 s
- Modèle recommandé : **Gradient Boosting**. Même performance que le Random Forest, environ 6 fois plus rapide.
- Facteurs les plus importants : `city_development_index`, puis `company_size` et `company_type` (surtout leurs valeurs vides).
- Attention : important pour le modèle ne veut pas dire cause du départ.