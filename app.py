import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV data
@st.cache_resource
def load_data():
    df = pd.read_csv("Trainingdata.csv")
    df['Bevölkerung'] = df['Bevölkerung'].str.replace(' ', '').astype(int)  # Remove spaces and convert to int
    return df

st.set_page_config(page_title="Bevölkerungszahl Deutschland")
st.write("Bevölkerungszahlen in Deutschland")
st.write("Willkommen zum Bevölkerungsdaten-Viewer.")

df = load_data()

# Init Session State
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.history = []
else:
    st.session_state.step += 1

input = st.text_input(label="Geben Sie eine Jahreszahl ein (1909 bis 2022):")

if input:
    try:
        year = int(input)
        population = df.loc[df['Jahr'] == year, 'Bevölkerung']
        if not population.empty:
            response = f"Die Bevölkerungszahl im Jahr {year} war {population.values[0]:,}."
        else:
            response = f"Keine Daten für das Jahr {year} gefunden."
    except ValueError:
        response = "Bitte geben Sie eine gültige Jahreszahl ein."
    
    st.session_state.history.append((input, response))

if st.button('Reset'):
    st.session_state.step = 0
    st.session_state.history = []

for entry in st.session_state.history:
    st.write("**Jahr**:", entry[0], "**Bevölkerung**:", entry[1])

# Plotting the data
fig, ax = plt.subplots()
df_sorted = df.sort_values('Jahr')
ax.bar(df_sorted['Jahr'], df_sorted['Bevölkerung'])
ax.set_xlabel('Jahr')
ax.set_ylabel('Bevölkerung')
ax.set_title('Bevölkerungszahl in Deutschland über die Jahre')
plt.xticks(rotation=90)

st.pyplot(fig)

st.write("Step: ", st.session_state.step)
