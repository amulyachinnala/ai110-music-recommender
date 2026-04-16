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
    """Loads songs from a CSV file and converts numerical strings to floats."""
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Casting logic: Convert specific keys to floats
            for key in ['energy', 'tempo_bpm', 'valence', 'danceability', 'acousticness']:
                row[key] = float(row[key])
            row['id'] = int(row['id'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Calculates a numeric score and provides a list of explanation strings."""
    score = 0.0
    reasons = []

    # 1. Genre Match (+2.0)
    if song['genre'].lower() == user_prefs['favorite_genre'].lower():
        score += 2.0
        reasons.append(f"Genre match: {song['genre']} (+2.0)")

    # 2. Mood Match (+1.0)
    if song['mood'].lower() == user_prefs['favorite_mood'].lower():
        score += 1.0
        reasons.append(f"Mood match: {song['mood']} (+1.0)")

    # 3. Energy Similarity (1.0 max)
    # 1.0 - absolute difference
    diff = abs(user_prefs['target_energy'] - song['energy'])
    energy_points = max(0.0, 1.0 - diff)
    score += energy_points
    if diff < 0.2:
        reasons.append(f"Energy affinity (+{energy_points:.1f})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Ranks the song catalog based on the scoring function."""
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        results.append((song, score, explanation))

    # Using sorted() creates a new list, leaving the original 'songs' catalog untouched.
    # We sort by the score (index 1) in descending order.
    return sorted(results, key=lambda x: x[1], reverse=True)[:k]
