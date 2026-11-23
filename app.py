import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Poubelle intelligente", page_icon="🗑️", layout="wide")

HORIZON = 4   # 4 mesures x 15 min = 1 heure
SEUIL = 80    # seuil d'alerte (%)


@st.cache_data
def charger(fichier):
    df = pd.read_csv(fichier, parse_dates=["date"])
    return df.sort_values("date").reset_index(drop=True)


def preparer(df):
    data = pd.DataFrame({
        "heure": df["date"].dt.hour + df["date"].dt.minute / 60,
        "jour_semaine": df["date"].dt.weekday,
        "niveau": df["niveau"],
        "niveau_prec": df["niveau"].shift(1),
        "niveau_futur": df["niveau"].shift(-HORIZON),
    })
    return data


@st.cache_resource
def entrainer(df):
    data = preparer(df).dropna()
    X = data[["heure", "jour_semaine", "niveau", "niveau_prec"]]
    y = data["niveau_futur"]
    coupure = int(len(data) * 0.8)
    modeles = {
        "Régression linéaire": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
    }
    scores = []
    for nom, m in modeles.items():
        m.fit(X.iloc[:coupure], y.iloc[:coupure])
        pred = m.predict(X.iloc[coupure:])
        scores.append({
            "Modèle": nom,
            "MAE": round(mean_absolute_error(y.iloc[coupure:], pred), 2),
            "R²": round(r2_score(y.iloc[coupure:], pred), 3),
        })
    # modèle final réentraîné sur toutes les données
    final = RandomForestRegressor(n_estimators=200, random_state=42).fit(X, y)
    return final, pd.DataFrame(scores)


st.title("🗑️ Poubelle intelligente")
st.caption("Suivi du remplissage et prédiction à 1 heure (données simulées)")

fichier = st.sidebar.file_uploader("Fichier CSV (colonnes : date, niveau)", type="csv")
if fichier is None:
    try:
        fichier = "donnees_poubelle.csv"
        df = charger(fichier)
    except FileNotFoundError:
        st.info("Charge ton fichier **donnees_poubelle.csv** dans le menu de gauche.")
        st.stop()
else:
    df = charger(fichier)

modele, scores = entrainer(df)

# --- Situation actuelle (dernière mesure) ---
prep = preparer(df)
derniere = prep.iloc[-1]
X_now = pd.DataFrame([derniere[["heure", "jour_semaine", "niveau", "niveau_prec"]]])
niveau_actuel = float(derniere["niveau"])
niveau_predit = float(modele.predict(X_now)[0])

c1, c2, c3 = st.columns(3)
c1.metric("Niveau actuel", f"{niveau_actuel:.0f} %")
c2.metric("Niveau prédit (+1 h)", f"{niveau_predit:.0f} %",
          f"{niveau_predit - niveau_actuel:+.1f} %")
c3.metric("Dernière mesure", df["date"].iloc[-1].strftime("%d/%m %H:%M"))

st.progress(min(int(niveau_actuel), 100))

if niveau_predit >= SEUIL:
    st.error(f"⚠️ Alerte : la poubelle sera à {niveau_predit:.0f} % dans 1 heure, "
             "pensez à la vider.")
else:
    st.success("✅ Pas d'alerte : le niveau prédit reste sous le seuil.")

# --- Historique ---
st.subheader("Historique du niveau")
jours = st.slider("Nombre de jours affichés", 1, 30, 7)
recent = df[df["date"] >= df["date"].iloc[-1] - pd.Timedelta(days=jours)]
graphique = recent.set_index("date")[["niveau"]].copy()
graphique["seuil"] = SEUIL
st.line_chart(graphique)

# --- Performances ---
st.subheader("Performance des modèles (jeu de test)")
st.dataframe(scores, hide_index=True)
st.caption("MAE : erreur moyenne en points de pourcentage. R² : proche de 1 = bonne prédiction.")
