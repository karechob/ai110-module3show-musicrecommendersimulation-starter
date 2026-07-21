import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted so we can do math on them later:
    - id and tempo_bpm become ints
    - energy, valence, danceability, acousticness become floats
    Text columns (title, artist, genre, mood) stay as strings.

    Required by src/main.py
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the Algorithm Recipe.

    Rules and weights:
      - Genre match:      +2.0  (exact match on favorite_genre)
      - Mood match:       +1.0  (exact match on favorite_mood)
      - Energy closeness: +1.0 * (1 - abs(song.energy - target_energy))
      - Acoustic fit:     +0.5  aligned with likes_acoustic

    Returns (score, reasons) where reasons is a list of human-readable
    strings explaining how each point was earned.
    """
    score = 0.0
    reasons: List[str] = []

    # Rule 1: Genre match (highest weight — strongest taste signal)
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Rule 2: Mood match
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Rule 3: Energy closeness — rewards being CLOSE to the target,
    # not just having a high value. Perfect match = +1.0, opposite = 0.
    energy_points = 1.0 * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target "
        f"{user_prefs['target_energy']:.2f} (+{energy_points:.2f})"
    )

    # Rule 4: Acoustic fit — reward high acousticness if the user likes
    # acoustic, otherwise reward low acousticness. Light tie-breaker weight.
    if user_prefs["likes_acoustic"]:
        acoustic_points = 0.5 * song["acousticness"]
        label = "likes acoustic"
    else:
        acoustic_points = 0.5 * (1 - song["acousticness"])
        label = "prefers non-acoustic"
    score += acoustic_points
    reasons.append(
        f"{label}: acousticness {song['acousticness']:.2f} (+{acoustic_points:.2f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks the whole catalog and returns the top k recommendations.

    Uses score_song() as the "judge" for every song, then sorts by score
    from highest to lowest and keeps the best k.

    Returns a list of (song_dict, score, explanation) tuples, where the
    explanation joins the per-song reasons into one readable string.
    """
    # Score every song in the catalog (list comprehension is the Pythonic loop).
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    # Ranking rule: sort highest score first. sorted() returns a NEW list and
    # leaves the input `songs` untouched; the lambda picks each tuple's score.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return ranked[:k]
