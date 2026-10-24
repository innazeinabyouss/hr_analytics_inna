from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report

from src.config import COLONNES_TEXTE, COLONNES_CHIFFRES

def preparer(df):
    """Garde les colonnes utiles et remplace les vides par 'Vide'."""
    X = df[COLONNES_TEXTE + COLONNES_CHIFFRES].copy()
    X[COLONNES_TEXTE] = X[COLONNES_TEXTE].fillna("Vide")
    return X


def entrainer_modele(df):
    """Entraîne un modèle qui prédit qui va partir, puis affiche sa note."""
    X = preparer(df)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    traduction = ColumnTransformer([
        ("texte", OneHotEncoder(handle_unknown="ignore"), COLONNES_TEXTE),
        ("chiffres", StandardScaler(), COLONNES_CHIFFRES),
    ])

    modele = Pipeline([
        ("traduction", traduction),
        ("modele", LogisticRegression(class_weight="balanced", max_iter=1000)),
    ])
    modele.fit(X_train, y_train)

    proba = modele.predict_proba(X_test)[:, 1]
    print("AUC :", round(roc_auc_score(y_test, proba), 3))
    print(classification_report(y_test, modele.predict(X_test)))
    return modele