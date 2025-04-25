
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel("popes_odds_completo.xlsx")
    return df

df = load_data()

st.title("🧾 Conclave Betting App")
st.markdown("Scommetti sul prossimo Papa!")

# Inizializzazione storico puntate
if "bets" not in st.session_state:
    st.session_state["bets"] = []

with st.expander("📊 Visualizza candidati e quote"):
    st.dataframe(df)

bet_type = st.selectbox("Scegli il tipo di scommessa", ["Nome", "Nazionalità", "Continente", "Fascia d’età"])

if bet_type == "Nome":
    scelta = st.selectbox("Scommetti su:", df["Name"])
elif bet_type == "Nazionalità":
    scelta = st.selectbox("Scommetti su:", df["Nazionalità"].unique())
elif bet_type == "Continente":
    scelta = st.selectbox("Scommetti su:", df["Continente"].unique())
elif bet_type == "Fascia d’età":
    scelta = st.selectbox("Scommetti su:", ["< 60", "60-70", "> 70"])

puntata = st.number_input("Inserisci la tua puntata (€)", min_value=1)

if st.button("📥 Conferma scommessa"):
    if bet_type == "Nome":
        quota = df[df["Name"] == scelta]["Odds"].values[0]
        vincita = round(puntata * quota, 2)
    elif bet_type == "Nazionalità":
        count = df[df["Nazionalità"] == scelta].shape[0]
        vincita = round(puntata * (len(df) / count), 2)
    elif bet_type == "Continente":
        count = df[df["Continente"] == scelta].shape[0]
        vincita = round(puntata * (len(df) / count), 2)
    elif bet_type == "Fascia d’età":
        if scelta == "< 60":
            count = df[df["Età"] < 60].shape[0]
        elif scelta == "60-70":
            count = df[(df["Età"] >= 60) & (df["Età"] <= 70)].shape[0]
        else:
            count = df[df["Età"] > 70].shape[0]
        vincita = round(puntata * (len(df) / count), 2)

    st.session_state["bets"].append({
        "Tipo": bet_type,
        "Scelta": scelta,
        "Puntata": puntata,
        "Potenziale Vincita": vincita
    })

    st.success(f"Hai scommesso su: {scelta}")
    st.info(f"Potenziale vincita: €{vincita}")

# Storico
st.subheader("🧾 Storico delle tue scommesse")
if st.session_state["bets"]:
    storico_df = pd.DataFrame(st.session_state["bets"])
    st.dataframe(storico_df)
else:
    st.info("Nessuna scommessa effettuata ancora.")

# Leaderboard
st.subheader("🏆 Leaderboard e Statistiche")
if st.session_state["bets"]:
    storico_df = pd.DataFrame(st.session_state["bets"])
    leaderboard = storico_df[storico_df["Tipo"] == "Nome"].groupby("Scelta")["Puntata"].sum().sort_values(ascending=False)

    if not leaderboard.empty:
        st.markdown("### 📈 Scommesse totali per Papa (in €)")
        st.bar_chart(leaderboard)
    else:
        st.info("Nessuna scommessa ancora su un singolo nome.")
else:
    st.info("Effettua una scommessa per vedere la leaderboard!")