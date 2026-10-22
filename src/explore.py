def controle_qualite(df):
    """Vérifie la santé des données : taille, doublons, vides, équilibre."""
    print("Taille :", df.shape)
    print("Doublons :", df.duplicated().sum())

    print("\n% de vides par colonne :")
    vides = (df.isnull().mean() * 100).round(1)
    print(vides.sort_values(ascending=False))

    print("\n% de chaque réponse (target) :")
    print((df["target"].value_counts(normalize=True) * 100).round(1))