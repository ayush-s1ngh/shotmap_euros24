# Import necessary libraries
import json
import pandas as pd
import streamlit as st

# Import VerticalPitch from mplsoccer library
from mplsoccer import VerticalPitch

# Set the title and subheader of the Streamlit app
st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all their shots taken!")

# Load the dataset from a CSV file
df = pd.read_csv('dataset_euros24.csv')

# Filter the dataset to only include shots
df = df[df['type'] == 'Shot'].reset_index(drop=True)

# Convert the 'location' column from string to JSON format
df['location'] = df['location'].apply(json.loads)

# Define a function to filter the data based on team and player
def filter_data(df: pd.DataFrame, team: str, player: str):
    """
    Filter the dataframe based on team and player.

    Args:
        df (pd.DataFrame): The input dataframe.
        team (str): The team to filter by.
        player (str): The player to filter by.

    Returns:
        pd.DataFrame: The filtered dataframe.
    """
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

# Define a function to plot the shots on the pitch
def plot_shots(df, ax, pitch):
    """
    Plot the shots on the pitch.

    Args:
        df (pd.DataFrame): The dataframe containing the shot data.
        ax (matplotlib Axes): The axes to plot on.
        pitch (VerticalPitch): The pitch to plot on.
    """
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['type'] == 'goal' else .5,
            zorder=2 if x['type'] == 'goal' else 1
        )

# Create select boxes for team and player
team = st.selectbox("Select a team", df['team'].sort_values().unique(), index=None)
player = st.selectbox("Select a player", df[df['team'] == team]['player'].sort_values().unique(), index=None)

# Filter the dataframe based on the selected team and player
filtered_df = filter_data(df, team, player)

# Create a VerticalPitch object
pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#f0f0f0', line_color='black', half=True)

# Create a figure and axes object
fig, ax = pitch.draw(figsize=(10, 10))

# Plot the shots on the pitch
plot_shots(filtered_df, ax, pitch)

# Display the plot using Streamlit
st.pyplot(fig)
