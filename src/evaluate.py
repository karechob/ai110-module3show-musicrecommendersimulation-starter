"""
System Evaluation harness for the Music Recommender.

Runs the recommender against several user profiles — three "normal" tastes
plus a few adversarial / edge-case profiles designed to see whether the
scoring logic can be tricked or produce unexpected results.

Run with:  python -m src.evaluate
"""

from src.recommender import load_songs, recommend_songs
from src.main import print_recommendations


# --- Three distinct "normal" taste profiles --------------------------------
NORMAL_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "likes_acoustic": False,
    },
}

# --- Adversarial / edge-case profiles --------------------------------------
# Each is designed to probe a specific weakness of the scoring logic.
EDGE_PROFILES = {
    # Conflicting vibe: lofi is calm/low-energy, but this user asks for
    # HIGH energy AND an "intense" mood AND acoustic. Nothing satisfies all.
    "Conflicting: High-Energy Acoustic Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": True,
    },
    # Nonexistent categories: no song has genre "reggae" or mood "sad",
    # so genre and mood rules can never fire — tests graceful fallback to
    # the continuous rules only.
    "Nonexistent: Reggae + Sad": {
        "favorite_genre": "reggae",
        "favorite_mood": "sad",
        "target_energy": 0.5,
        "likes_acoustic": False,
    },
    # Impossible combo: rock is high-energy and non-acoustic, but this user
    # wants calm (0.1) acoustic rock — the genre bonus and the continuous
    # rules pull in opposite directions.
    "Impossible: Calm Acoustic Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "relaxed",
        "target_energy": 0.1,
        "likes_acoustic": True,
    },
}


def run(profiles: dict, songs: list) -> None:
    for name, prefs in profiles.items():
        print(f"\n### Profile: {name}")
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(prefs, recommendations)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    print("\n" + "#" * 60)
    print("# NORMAL PROFILES")
    print("#" * 60)
    run(NORMAL_PROFILES, songs)

    print("\n" + "#" * 60)
    print("# ADVERSARIAL / EDGE-CASE PROFILES")
    print("#" * 60)
    run(EDGE_PROFILES, songs)


if __name__ == "__main__":
    main()
