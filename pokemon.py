import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import requests
import numpy as np

st.title("Pokemon Explorer!")

@st.cache
def get_all_id_numbers():
    return range(1, 899) 

def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        name = pokemon.get('name', 'Unknown')
        height = pokemon.get('height', np.nan)
        weight = pokemon.get('weight', np.nan)
        moves = len(pokemon.get('moves', []))
        sprite_url = pokemon.get('sprites', {}).get('front_default', '')
        poke_type = pokemon.get('types', [{}])[0].get('type', {}).get('name', '')
        poke_id = pokemon.get('id', np.nan)
        battle_cry_url = pokemon['cries']['latest']

        return name, height, weight, moves, sprite_url, poke_type, poke_id, battle_cry_url
    except:
        return 'Error', np.nan, np.nan, np.nan, '', '', np.nan, ''

pokemon_number = st.slider("Pick a pokemon",
                           min_value=1,
                           max_value=898 
                           )

name, height, weight, moves, sprite_url, poke_type, poke_id, battle_cry_url = get_details(pokemon_number)

height = height * 10
height_data = pd.DataFrame({'Pokemon': ['Weedle', name, 'Victreebel'],
                            'Heights': [30, height, 170]})

colors = ['gray', 'red', 'purple', 'blue', 'pink', 'brown', 'yellow', 'green']
graph = sns.barplot(data=height_data,
                    x='Pokemon',
                    y='Heights',
                    palette=colors * len(height_data))

st.write(f'Name: {name.title()}')
st.write(f'Height: {height}cm')
st.write(f'Weight: {weight}')
st.write(f'Move Count: {moves}')
st.write(f'Type: {poke_type}')

# Image of Pokemon
if sprite_url:
    st.image(sprite_url, caption= f'{name} in action!!')

# Audio of battle cry
if battle_cry_url:
    st.audio(battle_cry_url, format='audio/mpeg')
