import streamlit as st
import pandas as pd

st.set_page_config(page_title="Weekend Decathlon", layout="centered")

# --- DATA INITIALIZATION ---
players = ["Mathew Cowton", "Braeden Keyes", "Howie Keyes", "Khyle Marano", "Jesse Marano", "Adam Bice", "Jamie Kerby"]
events = ["⛳️ 9 Holes Golf", "🔫 Lazer Tag", "🍺 Pub Golf", "🎳 Lawn Bowls", "🃏 Blackjack", "🏓 Beer Pong", "🏉 NRL Bingo", "🎮 The Crew"]

if 'scores' not in st.session_state:
    st.session_state.scores = {p: 0 for p in players}
if 'pub_golf' not in st.session_state:
    st.session_state.pub_golf = pd.DataFrame(0, index=players, columns=[f"Hole {i+1}" for i in range(9)])

# --- SIDEBAR: THE $300 KITTY ---
with st.sidebar:
    st.header("💰 The Kitty")
    if 'kitty' not in st.session_state: st.session_state.kitty = 0.0
    st.metric("Total Pot", f"${st.session_state.kitty:.2f}")
    win = st.number_input("Blackjack Win ($)", min_value=0.0)
    if st.button("Add 50% Tax"):
        st.session_state.kitty += (win / 2)
        st.success("Pot Updated!")

# --- MAIN NAVIGATION ---
menu = st.tabs(["📊 Leaderboard", "🍺 Pub Golf Tracker", "🏆 Log Event"])

# --- TAB 1: LEADERBOARD ---
with menu[0]:
    st.header("Overall Standings")
    leaderboard_df = pd.DataFrame(list(st.session_state.scores.items()), columns=['Player', 'Points'])
    leaderboard_df = leaderboard_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    st.table(leaderboard_df)

# --- TAB 2: PUB GOLF TRACKER ---
with menu[1]:
    st.header("🍺 Pub Golf: Stroke Play")
    st.info("Record sips/gulps per hole. Lowest total wins the Decathlon points.")
    
    # Input for each player
    target_hole = st.selectbox("Select Current Hole", [f"Hole {i+1}" for i in range(9)])
    cols = st.columns(2)
    for i, p in enumerate(players):
        with cols[i % 2]:
            st.session_state.pub_golf.at[p, target_hole] = st.number_input(f"{p}'s Sips", min_value=0, key=f"{p}_{target_hole}")
    
    st.divider()
    st.subheader("Pub Golf Leaderboard")
    pg_totals = st.session_state.pub_golf.sum(axis=1).sort_values()
    st.write(pg_totals)
    
    if st.button("Finalize Pub Golf & Award Points"):
        winners = pg_totals.index.tolist()
        st.session_state.scores[winners[0]] += 10 # 1st
        st.session_state.scores[winners[1]] += 7  # 2nd
        st.session_state.scores[winners[2]] += 5  # 3rd
        st.success("Points added to Overall Leaderboard!")

# --- TAB 3: LOG OTHER EVENTS ---
with menu[2]:
    st.header("Log General Results")
    ev = st.selectbox("Select Event", [e for e in events if e != "🍺 Pub Golf"])
    g = st.selectbox("🥇 1st (10pts)", players, key="g")
    s = st.selectbox("🥈 2nd (7pts)", players, key="s")
    b = st.selectbox("🥉 3rd (5pts)", players, key="b")
    
    if st.button("Lock in Points"):
        st.session_state.scores[g] += 10
        st.session_state.scores[s] += 7
        st.session_state.scores[b] += 5
        st.balloons()