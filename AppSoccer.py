import numpy as np
import pandas as pd
import json
import streamlit as st
import unicodedata
from matplotlib import pyplot as plt
from Field import createPitch


# Create pitch plot
pitch_width = 120
pitch_height = 80
fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'gray')


# List of games and JSON files as dictionary
games_dict = {
    'Alavez': '15946',
    'Real Valladolid': '15956',
    'Huesca': '15973',
    'Real Sociedad': '15978',
    'Girona': '15986'
}

games_list = list(games_dict.keys())
games_id_list = list(games_dict.values())


# Set page config
st.set_page_config(page_title='F.C. Barcelona Game Stats', page_icon=':soccer:', initial_sidebar_state='expanded')

# Drop-down menu "Select Football Game"
st.sidebar.markdown('## Select Football Game')
menu_game = st.sidebar.selectbox('Select Game', games_list)
st.sidebar.markdown("""Here you can select one of 5 football games from the 2018/2019 La Liga Season: """)
st.sidebar.markdown(""" 
                    * Deportivo Alavez
                    * Real Valladolid FC
                    * Huesca FC
                    * Real Sociedad
                    * Girona FC
                    """)


# Read JSON file based on selected game
filename = ''+str(games_dict.get(menu_game))+'.json'
with open(filename, 'r', errors="ignore") as f:
    game = json.load(f)
df = pd.json_normalize(game, sep='_')


# Replace non-unicode characters in players names
df['player_name'] = df['player_name'].astype(str)
df['player_name'] = df['player_name'].apply\
    (lambda val: unicodedata.normalize('NFC', val).encode('ascii', 'ignore').decode('utf-8'))
df['player_name'] = df['player_name'].replace('nan', np.nan)


# Get teams and players names
team_1 = df['team_name'].unique()[0]
team_2 = df['team_name'].unique()[1]
mask_1 = df.loc[df['team_name'] == team_1]
mask_2 = df.loc[df['team_name'] == team_2]
player_names_1 = mask_1['player_name'].dropna().unique()
player_names_2 = mask_2['player_name'].dropna().unique()


# List of activities for drop-down menus
activities = ['Pass', 'Ball Receipt', 'Carry', 'Pressure', 'Shot']


# Drop-down menus 'Select Team, Player and Activity'
st.sidebar.markdown('## Select Player and Activity')
menu_team = st.sidebar.selectbox('Select Team', (team_1, team_2))
if menu_team == team_1:
    menu_player = st.sidebar.selectbox('Select Player', player_names_1)
else:
    menu_player = st.sidebar.selectbox('Select Player', player_names_2)
menu_activity = st.sidebar.selectbox('Select Activity', activities)
st.sidebar.markdown('Select a player and activity. Statistics plot will appear on the pitch.')


# Titles and text above the pitch
st.title('F.C. Barcelona Player Game Stats')
st.markdown("""
""")
st.write("""* Use dropdown-menus on the left side to select a game, team, player, and activity. 
Statistics plot will appear on the pitch below.""")
st.write('###', menu_activity, 'map')
st.write('###### Game:', menu_game)
st.write('###### Player:', menu_player, '(', menu_team, ')')


# Define five functions for five activities from drop-down menu
# Pass plot function
def pass_map():
    df_pass = df.loc[(df['player_name'] == menu_player) & (df['type_name'] == 'Pass')]
    location = df_pass['location'].tolist()
    pass_end_location = df_pass['pass_end_location'].tolist()
    color = 'blue' if menu_team == team_1 else 'red'
    if menu_team == team_1:
        x1 = np.array([el[0] for el in location])
        y1 = pitch_height-np.array([el[1] for el in location])
        x2 = np.array([el[0] for el in pass_end_location])
        y2 = pitch_height-np.array([el[1] for el in pass_end_location])
    else:
        x1 = pitch_width-np.array([el[0] for el in location])
        y1 = np.array([el[1] for el in location])
        x2 = pitch_width-np.array([el[0] for el in pass_end_location])
        y2 = np.array([el[1] for el in pass_end_location])
    u = x2-x1
    v = y2-y1
    ax.quiver(x1, y1, u, v, color=color, width=0.003, headlength=4.5)
    return ax


# Ball Receipt plot function
def ball_receipt_map():
    df_ball_rec = df.loc[(df['player_name'] == menu_player) & (df['type_name'] == 'Ball Receipt*')]
    location = df_ball_rec['location'].tolist()
    dot_size = 1
    color = 'blue' if menu_team == team_1 else 'red'
    if menu_team == team_1:
        x = np.array([el[0] for el in location])
        y = pitch_height-np.array([el[1] for el in location])
    else:
        x = pitch_width-np.array([el[0] for el in location])
        y = np.array([el[1] for el in location])
    for x, y in zip(x, y):
        dot = plt.Circle((x, y), dot_size, color=color, alpha=0.5)
        ax.add_patch(dot)
    return ax


# Carry plot function
def carry_map():
    df_carry = df.loc[(df['player_name'] == menu_player) & (df['type_name'] == 'Carry')]
    location = df_carry['location'].tolist()
    carry_end_location = df_carry['carry_end_location'].tolist()
    color = 'blue' if menu_team == team_1 else 'red'
    if menu_team == team_1:
        x1 = np.array([el[0] for el in location])
        y1 = pitch_height-np.array([el[1] for el in location])
        x2 = np.array([el[0] for el in carry_end_location])
        y2 = pitch_height-np.array([el[1] for el in carry_end_location])
    else:
        x1 = pitch_width-np.array([el[0] for el in location])
        y1 = np.array([el[1] for el in location])
        x2 = pitch_width-np.array([el[0] for el in carry_end_location])
        y2 = np.array([el[1] for el in carry_end_location])
    u = x2-x1
    v = y2-y1
    ax.quiver(x1, y1, u, v, color=color, width=0.003, headlength=4.5)
    return ax


# Pressure plot function
def pressure_map():
    df_pressure = df.loc[(df['player_name'] == menu_player) & (df['type_name'] == 'Pressure')]
    location = df_pressure['location'].tolist()
    dot_size = 2
    color = 'blue' if menu_team == team_1 else 'red'
    if menu_team == team_1:
        x = np.array([el[0] for el in location])
        y = pitch_height-np.array([el[1] for el in location])
    else:
        x = pitch_width-np.array([el[0] for el in location])
        y = np.array([el[1] for el in location])
    for x, y in zip(x, y):
        dot = plt.Circle((x, y), dot_size, color=color, alpha=0.5)
        ax.add_patch(dot)
    return ax


# Shot plot function
def shot_map():
    df_shot = df.loc[(df['player_name'] == menu_player) & (df['type_name'] == 'Shot')]
    location = df_shot['location'].tolist()
    color = 'blue' if menu_team == team_1 else 'red'
    if menu_team == team_1:
        x1 = np.array([el[0] for el in location])
        y1 = pitch_height-np.array([el[1] for el in location])
        x2 = np.full((len(x1)), 120)
        y2 = np.full((len(y1)), 40)
    else:
        x1 = pitch_width-np.array([el[0] for el in location])
        y1 = np.array([el[1] for el in location])
        x2 = np.full((len(x1)), 0)
        y2 = np.full((len(y1)), 40)
    u = x2-x1
    v = y2-y1
    ax.quiver(x1, y1, u, v, color=color, width=0.005, headlength=4.5)
    return ax


# Get plot function based on selected activity
if menu_activity == 'Pass':
    ax = pass_map()
elif menu_activity == 'Ball Receipt':
    ax = ball_receipt_map()
elif menu_activity == 'Carry':
    ax = carry_map()
elif menu_activity == 'Pressure':
    ax = pressure_map()
else:
    ax = shot_map()


# Plot the figure
plt.text(5, -3, team_1, size=15)
plt.text(100, -3, team_2, size=15)
fig.set_size_inches(15, 10)
st.pyplot(fig)


# Text underneath the pitch
st.write('##### Line-ups')
st.write(team_1, ':')
st.write(', '.join(str(e) for e in player_names_1))
st.write(team_2, ':')
st.write(', '.join(str(e) for e in player_names_2))
st.subheader('About this app')
st.markdown("""

This app displays player's statistics plotted on the pitch. Data is taken 
from StatsBomb Open Data at https://github.com/statsbomb/open-data

""")