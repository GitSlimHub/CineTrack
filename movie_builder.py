import streamlit as st  # <--- This is the library we need
import json
import random
import os
import requests
from datetime import datetime

# --- CONFIGURATION ---

API_KEY = st.secrets["GEMINI_API_KEY"] 
DATA_FILE = "my_movie_database.json"

# --- MASSIVE DATABASE (Static + Dynamic) ---
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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for that "App" feel
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        font-size: 18px;
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
    # Remove existing entry if present (to allow updates)
    st.session_state.user_movies = [m for m in st.session_state.user_movies if m['title'] != title]
    
    st.session_state.user_movies.append({
        "title": title,
        "rating": rating,
        "added_at": datetime.now().isoformat()
    })
    save_data()
    # Force refresh of current movie
    st.session_state.current_movie = None

def delete_movie(title):
    st.session_state.user_movies = [m for m in st.session_state.user_movies if m['title'] != title]
    save_data()

def get_stats():
    movies = st.session_state.user_movies
    return {
        "total": len(movies),
        "loved": len([m for m in movies if m['rating'] == 'loved']),
        "liked": len([m for m in movies if m['rating'] == 'liked']),
        "disliked": len([m for m in movies if m['rating'] == 'disliked']),
        "hated": len([m for m in movies if m['rating'] == 'hated']),
        "watchlist": len([m for m in movies if m['rating'] == 'watchlist'])
    }

def get_next_movie():
    seen_titles = {m['title'] for m in st.session_state.user_movies}
    # Combine static DB with any dynamic AI generated ones
    full_pool = HUGE_MOVIE_DATABASE + st.session_state.dynamic_pool
    
    available = [
        m for m in full_pool 
        if m not in seen_titles 
        and m not in st.session_state.skipped_session
    ]
    
    if not available:
        return None
    return random.choice(available)

# --- GEMINI AI FUNCTIONS ---
def call_gemini(prompt):
    if not API_KEY:
        st.error("API Key is missing. Please add it to the code.")
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        return json.loads(text)
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

def generate_unlimited_movies():
    seen_titles = [m['title'] for m in st.session_state.user_movies]
    prompt = f"""
      Generate a list of 20 popular, highly-rated movies from various genres.
      Do NOT include any of these: {', '.join(seen_titles[:100])}.
      Avoid these too: {', '.join(HUGE_MOVIE_DATABASE[:20])}.
      Return ONLY a JSON array of strings (titles).
    """
    with st.spinner("Consulting the infinite movie scroll..."):
        new_titles = call_gemini(prompt)
        if new_titles:
            st.session_state.dynamic_pool.extend(new_titles)
            # De-duplicate
            st.session_state.dynamic_pool = list(set(st.session_state.dynamic_pool))
            save_data()
            st.success(f"Added {len(new_titles)} new movies to the pool!")
            st.rerun()

# --- TABS ---
tab_rapid, tab_list, tab_watch, tab_ai, tab_add = st.tabs(["🔀 Rapid", "📋 List", "⏰ Watch", "✨ AI", "➕ Add"])

# === RAPID FIRE TAB ===
with tab_rapid:
    if st.session_state.current_movie is None:
        st.session_state.current_movie = get_next_movie()

    movie = st.session_state.current_movie

    if movie:
        st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{movie}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Have you seen this?</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Liked", key="btn_like"):
                add_rating(movie, "liked")
                st.rerun()
            if st.button("👎 Dislike", key="btn_dislike"):
                add_rating(movie, "disliked")
                st.rerun()
        
        with col2:
            if st.button("❤️ Loved", key="btn_love"):
                add_rating(movie, "loved")
                st.rerun()
            if st.button("😠 Hated", key="btn_hate"):
                add_rating(movie, "hated")
                st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            if st.button("⏰ Watch Later", key="btn_watch"):
                add_rating(movie, "watchlist")
                st.rerun()
        with col4:
            if st.button("⏭️ Skip", key="btn_skip"):
                st.session_state.skipped_session.add(movie)
                st.session_state.current_movie = None
                st.rerun()
                
    else:
        st.success("You have rated everything in the database!")
        if st.button("Generate Unlimited Movies (AI)"):
            generate_unlimited_movies()
        if st.button("Reset Skips"):
            st.session_state.skipped_session.clear()
            st.session_state.current_movie = None
            st.rerun()

    # Footer Stats
    st.divider()
    s = get_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Loved", s['loved'])
    c2.metric("Liked", s['liked'])
    c3.metric("Disliked", s['disliked'])
    c4.metric("Watched", s['total'])

# === LIST TAB ===
with tab_list:
    st.header("Your History")
    
    # Filter out watchlist items
    history = [m for m in st.session_state.user_movies if m['rating'] != 'watchlist']
    history.sort(key=lambda x: x['added_at'], reverse=True)
    
    if not history:
        st.info("No movies rated yet.")
    else:
        for m in history:
            c1, c2, c3 = st.columns([0.6, 0.2, 0.2])
            icon = {
                "loved": "❤️", "liked": "👍", 
                "disliked": "👎", "hated": "😠", "seen": "✔️"
            }.get(m['rating'], "?")
            
            c1.write(f"**{m['title']}**")
            c2.write(f"{icon} {m['rating'].upper()}")
            if c3.button("🗑️", key=f"del_{m['title']}"):
                delete_movie(m['title'])
                st.rerun()

# === WATCHLIST TAB ===
with tab_watch:
    st.header("Watchlist")
    watchlist = [m for m in st.session_state.user_movies if m['rating'] == 'watchlist']
    
    if not watchlist:
        st.info("Watchlist is empty.")
    else:
        for m in watchlist:
            c1, c2, c3 = st.columns([0.6, 0.2, 0.2])
            c1.write(f"**{m['title']}**")
            
            # Allow quick rating from watchlist
            if c2.button("Rate", key=f"rate_watch_{m['title']}"):
                # In a real app we'd open a modal, here we just move to rapid fire logic or remove
                # For simplicity, let's delete it so they can re-rate in Add tab, or we assume they watched it
                delete_movie(m['title']) 
                st.toast(f"Removed {m['title']} from watchlist")
                st.rerun()
                
            if c3.button("🗑️", key=f"del_w_{m['title']}"):
                delete_movie(m['title'])
                st.rerun()

# === AI TAB ===
with tab_ai:
    st.header("AI Insights ✨")
    
    option = st.selectbox("Choose AI Feature", ["Get Recommendations", "Roast My Taste", "Vibe Match", "Trivia"])
    
    if option == "Get Recommendations":
        if st.button("Generate Recs"):
            liked = [m['title'] for m in st.session_state.user_movies if m['rating'] in ['liked', 'loved']]
            seen = [m['title'] for m in st.session_state.user_movies]
            
            if len(liked) < 3:
                st.error("Rate at least 3 movies first!")
            else:
                prompt = f"""
                User likes: {', '.join(liked[-50:])}.
                Recommend 5 movies NOT in: {', '.join(seen)}.
                Return JSON schema: [{{'title': '', 'year': '', 'reason': '', 'emoji': ''}}]
                """
                with st.spinner("Thinking..."):
                    res = call_gemini(prompt)
                    if res:
                        for r in res:
                            st.success(f"{r['emoji']} **{r['title']}** ({r['year']})")
                            st.write(r['reason'])

    elif option == "Roast My Taste":
        if st.button("Roast Me"):
            user_list = [f"{m['title']} ({m['rating']})" for m in st.session_state.user_movies[-50:]]
            prompt = f"Roast this movie taste: {', '.join(user_list)}. Be snarky. Return JSON: {{'roast': 'text'}}"
            with st.spinner("Preparing insults..."):
                res = call_gemini(prompt)
                if res:
                    st.warning(f"🔥 {res['roast']}")

    elif option == "Vibe Match":
        vibe = st.text_input("What's the vibe?", placeholder="e.g. 80s sci-fi but funny")
        if st.button("Find Movie"):
            liked = [m['title'] for m in st.session_state.user_movies if m['rating'] in ['liked', 'loved']]
            prompt = f"""
            User likes: {', '.join(liked[-30:])}. Current vibe: "{vibe}".
            Recommend ONE perfect movie. Return JSON: {{'title': '', 'year': '', 'reason': '', 'emoji': ''}}
            """
            with st.spinner("Matching vibe..."):
                res = call_gemini(prompt)
                if res:
                    st.info(f"{res['emoji']} **{res['title']}** ({res['year']})")
                    st.write(res['reason'])

    elif option == "Trivia":
        if st.button("Generate Question"):
            loved = [m['title'] for m in st.session_state.user_movies if m['rating'] == 'loved']
            if not loved:
                st.error("Mark some movies as LOVED first!")
            else:
                prompt = f"""
                Pick one random movie: {', '.join(loved)}.
                Generate trivia. Return JSON: {{'movie': '', 'question': '', 'options': ['A','B','C','D'], 'correctIndex': 0, 'explanation': ''}}
                """
                with st.spinner("Generating trivia..."):
                    res = call_gemini(prompt)
                    if res:
                        st.session_state.trivia = res
        
        if 'trivia' in st.session_state:
            t = st.session_state.trivia
            st.subheader(f"Trivia: {t['movie']}")
            st.write(t['question'])
            
            ans = st.radio("Choose answer:", t['options'])
            if st.button("Submit Answer"):
                idx = t['options'].index(ans)
                if idx == t['correctIndex']:
                    st.balloons()
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! The answer was: {t['options'][t['correctIndex']]}")
                st.info(t['explanation'])

# === ADD TAB ===
with tab_add:
    st.header("Add Manually")
    new_title = st.text_input("Movie Title")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("👍 Liked"):
        if new_title: add_rating(new_title, "liked"); st.success(f"Added {new_title}");
    if c2.button("❤️ Loved"):
        if new_title: add_rating(new_title, "loved"); st.success(f"Added {new_title}");
    if c3.button("👎 Dislike"):
        if new_title: add_rating(new_title, "disliked"); st.success(f"Added {new_title}");
    if c4.button("😠 Hated"):
        if new_title: add_rating(new_title, "hated"); st.success(f"Added {new_title}");
    if c5.button("⏰ Watch"):
        if new_title: add_rating(new_title, "watchlist"); st.success(f"Added {new_title}");