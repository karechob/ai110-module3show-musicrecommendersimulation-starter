"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints a clean, readable layout: title, artist, score, and reasons."""
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"
    profile = (
        f"genre={user_prefs['favorite_genre']} | "
        f"mood={user_prefs['favorite_mood']} | "
        f"energy={user_prefs['target_energy']} | "
        f"acoustic={acoustic}"
    )

    print("=" * 60)
    print(f"🎵 Top {len(recommendations)} recommendations for your profile")
    print(f"   {profile}")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} — {song['artist']}")
        print(f"    Score: {score:.2f}")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      • {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
