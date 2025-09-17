import streamlit as st
import random
from math import comb

st.set_page_config(page_title='1Tap Mines Simulator', layout='centered')
st.title('💎 1Tap Mines Practice Simulator 💣')
st.markdown('**Practice your strategy with a 25-tile grid and 5 mines. Safe tiles in green, mines in red.**')

# Grid and mine settings
grid_size = 25
mines_count = 5
house_edge = 0.01

# Initialize mines and picked tiles
if 'mines' not in st.session_state:
    st.session_state.mines = set(random.sample(range(grid_size), mines_count))
if 'picked_tiles' not in st.session_state:
    st.session_state.picked_tiles = set()

# Helper functions
def success_probability(N, M, k):
    safe = N - M
    if k > safe: return 0.0
    return comb(safe, k)/comb(N, k)

def theoretical_multiplier(N, M, k, house_edge=0.01):
    p = success_probability(N, M, k)
    if p == 0: return 0.0
    return (1/p)*(1-house_edge)

# Display grid with clickable tiles
st.subheader('Click tiles to pick')
cols = st.columns(5)
for i in range(grid_size):
    col = cols[i%5]
    label = f'{i}'
    if i in st.session_state.picked_tiles:
        if i in st.session_state.mines:
            col.button(f'💣 {label}', key=i, disabled=True, help='Mine!')
        else:
            col.button(f'💎 {label}', key=i, disabled=True, help='Safe!')
    else:
        if col.button(label, key=f'pick{i}'):
            st.session_state.picked_tiles.add(i)

# Show current picks
safe_picks = [p for p in st.session_state.picked_tiles if p not in st.session_state.mines]
mined_picks = [p for p in st.session_state.picked_tiles if p in st.session_state.mines]

st.subheader('Your picks')
st.markdown(f'- **Safe picks:** {safe_picks}')
st.markdown(f'- **Mined picks:** {mined_picks}')

# Show multiplier
multiplier = theoretical_multiplier(grid_size, mines_count, len(safe_picks), house_edge)
st.markdown(f'**Theoretical multiplier:** {multiplier:.3f}x')

# Reveal all / reset round
if st.button('🔄 Reveal All & Reset Round'):
    st.session_state.mines = set(random.sample(range(grid_size), mines_count))
    st.session_state.picked_tiles = set()
    st.experimental_rerun()

# Style the grid visually with emojis and spacing
st.markdown('---')
st.markdown('**Legend:** 💎 Safe | 💣 Mine')
