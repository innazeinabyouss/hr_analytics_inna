import time
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, recall_score, precision_score
from sklearn.inspection import permutation_importance

from src.config import COLONNES_TEXTE, COLONNES_CHIFFRES


def preparer(df):
    """Garde les colonnes utiles et remplace les vides par 'Vide'."""
    X = df[COLONNES_TEXTE + COLONNES_CHIFFRES].copy()
    X[COLONNES_TEXTE] = X[COLONNES_TEXTE].fillna("Vide")
    return X


def decouper(df):
    """Sépare les données : 80 % pour apprendre, 20 % pour l'examen."""
    X = preparer(df)
    y = df["target"]
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


def creer_traduction():
    """Traduit le texte en chiffres et met les chiffres à la même échelle."""
    return ColumnTransformer([
        ("texte", OneHotEncoder(handle_unknown="ignore", sparse_output=False), COLONNES_TEXTE),
        ("chiffres", StandardScaler(), COLONNES_CHIFFRES),
    ])


MODELES = {
    "Régression logistique": LogisticRegression(class_weight="balanced", max_iter=1000),
    "Random Forest": RandomForestClassifier(
        n_estimators=300, min_samples_leaf=5, class_weight="balanced",
        random_state=42, n_jobs=-1),
    "Gradient Boosting": HistGradientBoostingClassifier(
        class_weight="balanced", random_state=42),
}


def creer_modele(nom):
    """Assemble la traduction et l'algorithme choisi."""
    return Pipeline([("traduction", creer_traduction()), ("modele", MODELES[nom])])

def comparer_modeles(df):
    """Entraîne plusieurs modèles sur le même découpage et compare leurs notes et leur vitesse."""
    X_train, X_test, y_train, y_test = decouper(df)
    for nom in MODELES:
        modele = creer_modele(nom)
        debut = time.perf_counter()
        modele.fit(X_train, y_train)
        duree = time.perf_counter() - debut
        proba = modele.predict_proba(X_test)[:, 1]
        pred = modele.predict(X_test)
        print(f"{nom:25} AUC {roc_auc_score(y_test, proba):.3f}"
              f" | recall {recall_score(y_test, pred):.2f}"
              f" | precision {precision_score(y_test, pred):.2f}"
              f" | {duree:.1f} s")


def valider_modeles(df):
    """Fait passer 5 examens différents à chaque modèle et donne la note moyenne."""
    X = preparer(df)
    y = df["target"]
    decoupage = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for nom in MODELES:
        notes = cross_val_score(creer_modele(nom), X, y, cv=decoupage, scoring="roc_auc")
        print(f"{nom:25} AUC moyenne {notes.mean():.3f} (± {notes.std():.3f})")


def importance_colonnes(df, nom="Gradient Boosting"):
    """Mesure quelles colonnes comptent le plus pour le modèle choisi."""
    X_train, X_test, y_train, y_test = decouper(df)
    modele = creer_modele(nom)
    modele.fit(X_train, y_train)
    resultat = permutation_importance(
        modele, X_test, y_test, scoring="roc_auc", n_repeats=5, random_state=42
    )
    importance = pd.Series(resultat.importances_mean, index=X_test.columns)
    return importance.sort_values(ascending=False).round(3)