"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")

    print(f"{'='*110}")
    print(f"{'TITLE':<20} | {'SCORE':<7} | {'REASONING'}")
    print(f"{'='*110}")
    for song, score, reason in recommendations:
        print(f"{song['title']:<20} | {score:<7} | {reason}")
    print(f"{'='*110}\n")

if __name__ == "__main__":
    main()
