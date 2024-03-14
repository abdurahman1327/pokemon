import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import requests
import numpy as np

# color based on Pokemon type
def get_pokemon_color():
    type_color_map = {
        'grass': 'green',
        'fire': 'orange',
        'water': 'blue',
        'electric': 'yellow',
        'rock': 'brown',
        'ground': 'tan',
        'poison': 'purple',
        'fairy': 'pink',
        'dragon': 'cyan',
        'psychic': 'magenta',
        'bug': 'lime',
        'flying': 'skyblue',
        'fighting': 'red',
        'normal': 'lightgray',
        'ice': 'lightblue',
        'ghost': 'darkviolet',
        'dark': 'black',
        'steel': 'gray'
    }
    return type_color_map

# Function to fetch Pokemon details
@st.cache_data
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
        battle_cry_url = pokemon.get('cries', {}).get('latest', '')

        return name, height, weight, moves, sprite_url, poke_type, poke_id, battle_cry_url
    except:
        return 'Error', np.nan, np.nan, np.nan, '', '', np.nan, ''

@st.cache_data
def get_all_id_numbers():
    return range(1, 899) 

# title
st.title("Pokemon Explorer")

# filter Pokemon types
selected_type = st.sidebar.selectbox("Select Pokemon Type", ['All'] + list(get_pokemon_color().keys()))  # No need to pass any argument

# Pokemon IDs based on type
if selected_type == 'All':
    selected_ids = get_all_id_numbers()
else:
    selected_ids = [poke_id for poke_id in get_all_id_numbers() if get_details(poke_id)[5] == selected_type]

# Pokemon card details
column1, column2 = st.columns(2)

with column1:
    st.header("Explore Pokemon")
    for poke_id in selected_ids:
        name, height, weight, moves, sprite_url, poke_type, poke_id, battle_cry_url = get_details(poke_id)
        poke_color = get_pokemon_color()[poke_type] if poke_type in get_pokemon_color() else 'gray'
        
        # Display Pokemon card
        with st.container():
            st.image(sprite_url, caption=f"{name.title()} - ID: {poke_id}", width=150)
            st.markdown(f"**Name:** {name.title()}  \n**Type:** {poke_type.title()}  \n**Height:** {height} cm  \n**Weight:** {weight}  \n**Moves:** {moves}")
            if battle_cry_url:
                st.audio(battle_cry_url, format='audio/mpeg')
            st.write('---')

with column2:
    st.header("Height vs. Weight Scatter Plot")
    pokemon_data = pd.DataFrame(columns=['Name', 'Height', 'Weight', 'Type'])

    for poke_id in selected_ids:
        name, height, weight, _, _, poke_type, _, _ = get_details(poke_id)
        pokemon_data = pokemon_data.append({'Name': name.title(), 'Height': height, 'Weight': weight, 'Type': poke_type}, ignore_index=True)

    sns.set_style("whitegrid")
    sns.scatterplot(data=pokemon_data, x='Height', y='Weight', hue='Type', palette=get_pokemon_color(), s=100, alpha=0.7)
    plt.title("Pokemon Height vs. Weight")
    plt.xlabel("Height (cm)")
    plt.ylabel("Weight (kg)")
    plt.legend(title='Type')
    st.pyplot(plt)

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "Built with Streamlit by Abdurahman")
