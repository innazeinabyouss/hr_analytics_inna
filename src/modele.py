from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, recall_score, precision_score

from src.config import COLONNES_TEXTE, COLONNES_CHIFFRES


def preparer(df):
    """Garde les colonnes utiles et remplace les vides par 'Vide'."""
    X = df[COLONNES_TEXTE + COLONNES_CHIFFRES].copy()
    X[COLONNES_TEXTE] = X[COLONNES_TEXTE].fillna("Vide")
    return X


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


def comparer_modeles(df):
    """Entraîne plusieurs modèles sur le même découpage et compare leurs notes."""
    X = preparer(df)
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    for nom, algo in MODELES.items():
        modele = Pipeline([("traduction", creer_traduction()), ("modele", algo)])
        modele.fit(X_train, y_train)
        proba = modele.predict_proba(X_test)[:, 1]
        pred = modele.predict(X_test)
        print(f"{nom:25} AUC {roc_auc_score(y_test, proba):.3f}"
              f" | recall {recall_score(y_test, pred):.2f}"
              f" | precision {precision_score(y_test, pred):.2f}")