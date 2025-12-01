import streamlit as st
import json
import random
import os
import requests
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = st.secrets["GEMINI_API_KEY"]

DATA_FILE = "my_movie_database.json"

# --- MASSIVE DATABASE ---
HUGE_MOVIE_DATABASE = [
    "The Matrix", "Terminator 2: Judgment Day", "Mad Max: Fury Road", "Inception", 
    "The Dark Knight", "Blade Runner 2049", "Dune: Part One", "Dune: Part Two", "Aliens", 
    "Star Wars: A New Hope", "Empire Strikes Back", "Return of the Jedi", "Jurassic Park", 
    "Avatar", "Avatar: The Way of Water", "Gladiator", "300", "V for Vendetta", "District 9", 
    "Minority Report", "Edge of Tomorrow", "Logan", "Deadpool", "Iron Man", "The Avengers",
    "Captain America: The Winter Soldier", "Black Panther", "Spider-Man 2", "Spider-Man: No Way Home",
    "Casino Royale", "Skyfall", "Mission: Impossible - Fallout", "Mission: Impossible - Dead Reckoning",
    "John Wick", "John Wick: Chapter 4", "Die Hard", "The Fifth Element", "Predator", "RoboCop", 
    "Total Recall", "Starship Troopers", "12 Monkeys", "Children of Men", "Snowpiercer", 
    "Looper", "Pacific Rim", "Rise of the Planet of the Apes", "Dawn of the Planet of the Apes", 
    "Dredd", "The Raid: Redemption", "The Raid 2", "Kill Bill: Vol. 1", "Kill Bill: Vol. 2",
    "Speed", "Face/Off", "The Rock", "Con Air", "Independence Day", "Men in Black", 
    "Guardians of the Galaxy", "Thor: Ragnarok", "X-Men: Days of Future Past",
    "Rogue One: A Star Wars Story", "The Batman", "Top Gun", "Top Gun: Maverick",
    "Extraction", "The Grey", "Nobody", "Atomic Blonde", "Bullet Train", "Monkey Man",
    "Civil War", "Furiosa: A Mad Max Saga", "The Creator", "Godzilla Minus One",
    "Se7en", "Fight Club", "Pulp Fiction", "Reservoir Dogs", "Goodfellas", 
    "The Godfather", "The Godfather Part II", "Scarface", "Heat", "The Departed", 
    "Prisoners", "Sicario", "No Country for Old Men", "Zodiac", "Shutter Island", 
    "Gone Girl", "The Silence of the Lambs", "American Psycho", "Drive", 
    "Nightcrawler", "Joker", "Taxi Driver", "Snatch", "Lock, Stock and Two Smoking Barrels", 
    "Training Day", "The Usual Suspects", "L.A. Confidential", "Fargo", "Casino", 
    "A Bronx Tale", "Donnie Brasco", "Carlito's Way", "American Gangster", "Collateral", 
    "Inside Man", "Ocean's Eleven", "Sherlock Holmes", "Knives Out", "Glass Onion", 
    "Wind River", "Hell or High Water", "Blue Ruin", "Green Room", "Uncut Gems", 
    "Good Time", "Memories of Murder", "Oldboy (2003)", "Parasite", "The Handmaiden", 
    "I Saw the Devil", "The Chaser", "Infernal Affairs", "Hard Boiled", "The Killer",
    "Chinatown", "Double Indemnity", "The Maltese Falcon", "Touch of Evil", "The Third Man",
    "Cape Fear", "Mystic River", "Primal Fear", "The Game", "Panic Room", "Source Code",
    "The Town", "Baby Driver", "Den of Thieves", "Wrath of Man", "The Gentlemen",
    "Promising Young Woman", "Saltburn", "Anatomy of a Fall", "The Killer (2023)",
    "War Dogs",
    "The Shawshank Redemption", "Forrest Gump", "The Prestige", "Memento",
    "Interstellar", "Arrival", "Eternal Sunshine of the Spotless Mind", 
    "The Truman Show", "Requiem for a Dream", "Black Swan", "American Beauty", 
    "There Will Be Blood", "Whiplash", "La La Land", "Birdman", "The Grand Budapest Hotel", 
    "Moonrise Kingdom", "Her", "Lost in Translation", "Good Will Hunting", 
    "Dead Poets Society", "A Beautiful Mind", "Slumdog Millionaire", "The Social Network", 
    "Spotlight", "12 Years a Slave", "Moonlight", "Schindler's List", "The Pianist", 
    "Life is Beautiful", "City of God", "Pan's Labyrinth", "Amélie", "Roma",
    "Manchester by the Sea", "Marriage Story", "Three Billboards Outside Ebbing, Missouri",
    "The Banshees of Inisherin", "Tár", "The Whale", "Oppenheimer", "Killers of the Flower Moon",
    "Poor Things", "Past Lives", "The Zone of Interest", "Anora", "The Holdovers",
    "Little Miss Sunshine", "Juno", "Lady Bird", "Frances Ha", "Mid90s", "Eighth Grade",
    "The Florida Project", "A Ghost Story", "Aftersun", "Minari", "Nomadland",
    "Everything Everywhere All At Once", "The Green Knight", "A Clockwork Orange",
    "2001: A Space Odyssey", "Barry Lyndon", "Eyes Wide Shut", "Magnolia", "Boogie Nights",
    "Phantom Thread", "Licorice Pizza", "The Master", "Midsommar", "Hereditary", 
    "The Witch", "The Lighthouse", "Beau Is Afraid", "Get Out", "Us", "Nope",
    "Saving Private Ryan", "Apocalypse Now", "Full Metal Jacket", 
    "Inglourious Basterds", "Hacksaw Ridge", "Dunkirk", "1917", 
    "All Quiet on the Western Front", "Platoon", "Black Hawk Down", 
    "Enemy at the Gates", "Fury", "The Imitation Game", "Darkest Hour",
    "Braveheart", "Kingdom of Heaven", "Troy", "Master and Commander",
    "The Last of the Mohicans", "Glory", "Letters from Iwo Jima", "Jarhead",
    "American Sniper", "Zero Dark Thirty", "Lone Survivor", "The Hurt Locker",
    "Lawrence of Arabia", "Bridge on the River Kwai", "Patton", "Das Boot",
    "Come and See", "Schindler's List", "Downfall", "The Zone of Interest",
    "Superbad", "The Hangover", "Step Brothers", "The Big Lebowski", "Office Space",
    "Shaun of the Dead", "Hot Fuzz", "The World's End", "Zombieland", "Tropic Thunder",
    "Anchorman", "Borat", "Mean Girls", "Clueless", "Ferris Bueller's Day Off",
    "The Breakfast Club", "Back to the Future", "Ghostbusters", "Groundhog Day", 
    "Beetlejuice", "Edward Scissorhands", "The Nightmare Before Christmas",
    "Napoleon Dynamite", "School of Rock", "Elf", "Wedding Crashers", "Old School",
    "Dodgeball", "Zoolander", "Talladega Nights", "The Other Guys", "21 Jump Street",
    "Game Night", "Horrible Bosses", "Bridesmaids", "Pitch Perfect", "Barbie",
    "Paddington 2", "Wonka", "Dungeons & Dragons: Honor Among Thieves",
    "Scott Pilgrim vs. the World", "Kick-Ass", "Kingsman: The Secret Service",
    "Monty Python and the Holy Grail", "Life of Brian", "Airplane!", "The Naked Gun",
    "Young Frankenstein", "Blazing Saddles", "Spaceballs", "Galaxy Quest",
    "Spirited Away", "Princess Mononoke", "My Neighbor Totoro", "Howl's Moving Castle",
    "Akira", "Ghost in the Shell", "Perfect Blue", "Paprika", "Your Name", "Weathering With You",
    "Suzume", "The Boy and the Heron", "Spider-Man: Into the Spider-Verse", 
    "Spider-Man: Across the Spider-Verse", "The Lion King", "Beauty and the Beast", 
    "Aladdin", "Mulan", "Toy Story", "Toy Story 2", "Toy Story 3", "The Incredibles",
    "Ratatouille", "Wall-E", "Up", "Inside Out", "Coco", "Soul", "Finding Nemo",
    "Monsters, Inc.", "Shrek", "Shrek 2", "Kung Fu Panda", "How to Train Your Dragon",
    "The Lego Movie", "Puss in Boots: The Last Wish", "The Iron Giant", "Fantastic Mr. Fox",
    "Isle of Dogs", "Coraline", "Kubo and the Two Strings", "Teenage Mutant Ninja Turtles: Mutant Mayhem",
    "The Shining", "The Exorcist", "Halloween", "A Nightmare on Elm Street", "Scream",
    "The Thing", "Alien", "Jaws", "Psycho", "The Texas Chain Saw Massacre",
    "The Cabin in the Woods", "It Follows", "The Babadook", "Hereditary", "Midsommar",
    "The Witch", "Get Out", "Us", "Nope", "A Quiet Place", "The Conjuring", "Sinister",
    "Insidious", "Barbarian", "Smile", "Talk to Me", "X", "Pearl", "MaXXXine",
    "28 Days Later", "Train to Busan", "Dawn of the Dead (2004)", "Shaun of the Dead",
    "Evil Dead II", "Army of Darkness", "Evil Dead Rise", "Suspiria", "Raw", "Titane"
]

# --- APP SETUP ---
st.set_page_config(
    page_title="CineTrack", 
    page_icon="🎬", 
    layout="centered", # Better for mobile than "wide"
    initial_sidebar_state="collapsed"
)

# --- MOBILE CSS INJECTION ---
st.markdown("""
    <style>
    /* Remove padding to use more screen space */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Make buttons huge and touch-friendly */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        height: 4.5em; /* Taller buttons for thumbs */
        font-weight: 800;
        font-size: 18px;
        border: 1px solid #333;
        transition: transform 0.1s;
    }
    
    /* Button click effect */
    .stButton>button:active {
        transform: scale(0.98);
    }

    /* Tabs at TOP (Default Streamlit behavior restored, just styled) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 10px 0px;
        border-bottom: 1px solid #333;
        justify-content: space-around;
        border-radius: 0px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 5px;
        color: #888;
        font-size: 12px;
        flex: 1;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #262730;
        color: #FFD700;
    }
    
    /* Hide the default hamburger menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Card Style for List */
    .movie-card {
        background-color: #1c1c1c;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #333;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA PERSISTENCE ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"movies": [], "dynamic_pool": []}

def save_data():
    data = {
        "movies": st.session_state.user_movies,
        "dynamic_pool": st.session_state.dynamic_pool
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# --- INIT SESSION STATE ---
if 'user_movies' not in st.session_state:
    data = load_data()
    st.session_state.user_movies = data["movies"]
    st.session_state.dynamic_pool = data.get("dynamic_pool", [])

if 'current_movie' not in st.session_state:
    st.session_state.current_movie = None

if 'skipped_session' not in st.session_state:
    st.session_state.skipped_session = set()

# --- HELPER FUNCTIONS ---
def add_rating(title, rating):
    st.session_state.user_movies = [m for m in st.session_state.user_movies if m['title'] != title]
    st.session_state.user_movies.append({
        "title": title,
        "rating": rating,
        "added_at": datetime.now().isoformat()
    })
    save_data()
    st.session_state.current_movie = None

def delete_movie(title):
    st.session_state.user_movies = [m for m in st.session_state.user_movies if m['title'] != title]
    save_data()

def get_next_movie():
    seen_titles = {m['title'] for m in st.session_state.user_movies}
    full_pool = HUGE_MOVIE_DATABASE + st.session_state.dynamic_pool
    available = [m for m in full_pool if m not in seen_titles and m not in st.session_state.skipped_session]
    if not available:
        return None
    return random.choice(available)

# --- GEMINI AI FUNCTIONS ---
def call_gemini(prompt):
    if not API_KEY:
        st.error("API Key missing. Check code.")
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
    try:
        response = requests.post(url, headers=headers, json=payload)
        return json.loads(response.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        return None

def generate_unlimited_movies():
    seen = [m['title'] for m in st.session_state.user_movies]
    prompt = f"Generate 20 popular movie titles. Exclude: {', '.join(seen[:50])}. Return JSON array of strings."
    with st.spinner("Finding new movies..."):
        res = call_gemini(prompt)
        if res:
            st.session_state.dynamic_pool.extend(res)
            st.session_state.dynamic_pool = list(set(st.session_state.dynamic_pool))
            save_data()
            st.rerun()

# --- MAIN APP UI ---

# We use tabs at the top now
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 Play", "📋 List", "⏰ Watch", "✨ AI", "➕ Add"])

# === RAPID FIRE TAB ===
with tab1:
    if st.session_state.current_movie is None:
        st.session_state.current_movie = get_next_movie()

    movie = st.session_state.current_movie

    if movie:
        st.markdown(f"<div style='text-align:center; padding: 20px 0;'><h1 style='color:#FFD700; margin-bottom:0;'>{movie}</h1><p style='color:#666;'>Have you seen this?</p></div>", unsafe_allow_html=True)
        
        # ROW 1: POSITIVE ACTIONS (Like & Love)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👍 LIKE", key="rf_like", type="primary"):
                add_rating(movie, "liked")
                st.rerun()
        with c2:
            if st.button("❤️ LOVE", key="rf_love", type="primary"):
                add_rating(movie, "loved")
                st.rerun()

        # ROW 2: NEGATIVE ACTIONS (Dislike & Hate)
        c3, c4 = st.columns(2)
        with c3:
            if st.button("👎 DISLIKE", key="rf_dislike"):
                add_rating(movie, "disliked")
                st.rerun()
        with c4:
            if st.button("😠 HATE", key="rf_hate"):
                add_rating(movie, "hated")
                st.rerun()

        # Secondary Actions (Full Width)
        st.write("") # Spacer
        c5, c6 = st.columns(2)
        with c5:
            if st.button("⏰ Watchlist", key="rf_watch"):
                add_rating(movie, "watchlist")
                st.rerun()
        with c6:    
            if st.button("⏭️ Skip", key="rf_skip"):
                st.session_state.skipped_session.add(movie)
                st.session_state.current_movie = None
                st.rerun()
            
    else:
        st.info("🎉 Database empty!")
        if st.button("Load More Movies (AI)", type="primary"):
            generate_unlimited_movies()
        if st.button("Reset Skips"):
            st.session_state.skipped_session.clear()
            st.rerun()

# === LIST TAB ===
with tab2:
    st.markdown("### 🎬 History")
    history = [m for m in st.session_state.user_movies if m['rating'] != 'watchlist']
    history.sort(key=lambda x: x['added_at'], reverse=True)
    
    if not history:
        st.caption("No history yet.")
    
    for m in history:
        icon = {"loved": "❤️", "liked": "👍", "disliked": "👎", "hated": "😠"}.get(m['rating'], "?")
        col_txt, col_del = st.columns([0.85, 0.15])
        with col_txt:
            st.markdown(f"<div class='movie-card'><b>{m['title']}</b><span>{icon}</span></div>", unsafe_allow_html=True)
        with col_del:
            if st.button("✖️", key=f"del_{m['title']}"):
                delete_movie(m['title'])
                st.rerun()

# === WATCHLIST TAB ===
with tab3:
    st.markdown("### ⏰ Watchlist")
    watchlist = [m for m in st.session_state.user_movies if m['rating'] == 'watchlist']
    
    if not watchlist:
        st.caption("Nothing to watch yet.")
        
    for m in watchlist:
        st.markdown(f"**{m['title']}**")
        c_rate, c_del = st.columns(2)
        with c_rate:
            if st.button("Mark Watched", key=f"w_rate_{m['title']}"):
                delete_movie(m['title']) # Quick logic: remove from watchlist to rate in Add tab
                st.toast("Moved to history (rate it in Add tab)")
                st.rerun()
        with c_del:
            if st.button("Remove", key=f"w_del_{m['title']}"):
                delete_movie(m['title'])
                st.rerun()
        st.divider()

# === AI TAB ===
with tab4:
    st.markdown("### ✨ AI Insights")
    mode = st.radio("Select Mode", ["Recs", "Roast", "Vibe", "Trivia"], horizontal=True, label_visibility="collapsed")
    
    if mode == "Recs":
        if st.button("Get Recommendations", type="primary"):
            liked = [m['title'] for m in st.session_state.user_movies if m['rating'] in ['liked', 'loved']]
            if len(liked) < 3:
                st.error("Rate more movies first!")
            else:
                prompt = f"User likes: {', '.join(liked[-30:])}. Recommend 5 movies. Return JSON: [{{'title':'', 'reason':''}}]"
                with st.spinner("Thinking..."):
                    res = call_gemini(prompt)
                    if res:
                        for r in res:
                            st.success(f"**{r['title']}**")
                            st.caption(r['reason'])

    elif mode == "Roast":
        if st.button("Roast My Taste", type="primary"):
            user_list = [f"{m['title']} ({m['rating']})" for m in st.session_state.user_movies[-30:]]
            prompt = f"Roast this taste: {', '.join(user_list)}. Be snarky. Return JSON: {{'roast': 'text'}}"
            with st.spinner("Preparing insult..."):
                res = call_gemini(prompt)
                if res:
                    st.error(f"🔥 {res['roast']}")

    elif mode == "Vibe":
        vibe = st.text_input("I'm in the mood for...", placeholder="e.g. 80s sci-fi but funny")
        if st.button("Find Movie"):
            prompt = f"Recommend ONE movie for vibe: '{vibe}'. Return JSON: {{'title':'', 'reason':''}}"
            with st.spinner("Searching..."):
                res = call_gemini(prompt)
                if res:
                    st.info(f"🎥 **{res['title']}**")
                    st.write(res['reason'])

    elif mode == "Trivia":
        if st.button("New Question"):
            loved = [m['title'] for m in st.session_state.user_movies if m['rating'] == 'loved']
            if not loved:
                st.error("Love some movies first!")
            else:
                prompt = f"Trivia for: {random.choice(loved)}. JSON: {{'q':'', 'options':['a','b'], 'correct':0}}"
                res = call_gemini(prompt)
                if res:
                    st.session_state.trivia = res
        
        if 'trivia' in st.session_state:
            t = st.session_state.trivia
            st.write(f"**Q:** {t['q']}")
            ans = st.radio("Answer:", t['options'])
            if st.button("Check"):
                if t['options'].index(ans) == t['correct']:
                    st.balloons()
                    st.success("Correct!")
                else:
                    st.error("Wrong!")

# === ADD TAB ===
with tab5:
    st.markdown("### ➕ Add Manually")
    new_title = st.text_input("Movie Title", placeholder="Type movie name...")
    
    # 2x2 Grid for Ratings
    r1, r2 = st.columns(2)
    with r1:
        if st.button("👍 Liked", key="add_like"):
            if new_title: add_rating(new_title, "liked"); st.success("Added!");
        if st.button("👎 Dislike", key="add_dis"):
            if new_title: add_rating(new_title, "disliked"); st.success("Added!");
            
    with r2:
        if st.button("❤️ Loved", key="add_love"):
            if new_title: add_rating(new_title, "loved"); st.success("Added!");
        if st.button("😠 Hated", key="add_hate"):
            if new_title: add_rating(new_title, "hated"); st.success("Added!");
            
    if st.button("⏰ Add to Watchlist", key="add_watch", type="primary"):
        if new_title: add_rating(new_title, "watchlist"); st.success("Saved!");
