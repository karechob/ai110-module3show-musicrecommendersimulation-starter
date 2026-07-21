# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Real-world recommenders like Spotify and YouTube predict what you'll enjoy next using two main ideas: collaborative filtering, which learns from the behavior of millions of users ("people who liked what you like also liked this") to capture taste that's hard to describe but needs lots of listening data, and content-based filtering, which looks at the measurable attributes of each song and recommends ones whose attributes match your preferences — which is how a brand-new track can be suggested before anyone has played it. My version is a small content-based recommender, because I have a song catalog but no user listening history, so I score each song by how well its features match a user's taste profile; each Song uses its genre, mood, energy, and acousticness for scoring (with id, title, and artist only for display, and tempo_bpm, valence, and danceability reserved for later experiments), and each UserProfile mirrors these with favorite_genre, favorite_mood, target_energy, and likes_acoustic. It prioritizes genre first as the strongest signal of taste, then mood, then how close a song's energy is to the user's target (rewarding closeness rather than just higher values), and finally whether its acousticness fits — producing recommendations that are transparent and easy to explain, at the cost of the surprising discoveries that collaborative filtering provides.

## Algorithm Recipe

My recommender scores every song against a user's taste profile using four
weighted rules, then ranks all songs by their total score and returns the top k.

**User profile fields:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

**Scoring rules (per song):**

| Rule | Weight | How points are earned |
|------|--------|-----------------------|
| Genre match   | **+2.0** | Full points if the song's genre equals the user's favorite genre |
| Mood match    | **+1.0** | Full points if the song's mood equals the user's favorite mood |
| Energy closeness | **+1.0** | `1 - abs(song.energy - target_energy)` — rewards being *close* to the target, not just high |
| Acoustic fit  | **+0.5** | Rewards high acousticness if `likes_acoustic` is true, low acousticness if false |

**Total score = genre + mood + energy + acoustic**, ranging from **0 to 4.5**.

**Ranking rule:** score every song, sort by total score (highest first), return the top k.

The weights encode my priority order: **genre matters most, mood and energy are
equal partners, and acousticness is a light tie-breaker.**

## Potential Biases

- **Genre over-prioritization.** Because genre is worth 2× any other rule, the system
  may bury a song that perfectly matches the user's mood and energy simply because its
  genre is "wrong" — ignoring great cross-genre songs a real listener might love.
- **Exact-match rigidity.** Genre and mood only reward *identical* matches, so closely
  related tastes (e.g. "chill" vs "relaxed", or "rock" vs "synthwave") count for nothing,
  even though they are musically similar.
- **No mixed taste.** The profile allows only one favorite genre and one mood, so a user
  who likes both intense rock and chill lofi cannot be represented accurately.
- **Popularity & catalog blind spots.** The system can only recommend from a tiny 10–18
  song catalog and knows nothing about lyrics, language, or artist diversity — so
  underrepresented genres and moods simply never surface.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Loaded songs: 18

============================================================
🎵 Top 5 recommendations for your profile
   genre=pop | mood=happy | energy=0.8 | acoustic=no
============================================================

#1  Sunrise City — Neon Echo
    Score: 4.39
    Why:
      • genre match: pop (+2.0)
      • mood match: happy (+1.0)
      • energy 0.82 vs target 0.80 (+0.98)
      • prefers non-acoustic: acousticness 0.18 (+0.41)

#2  Power Sprint — Max Pulse
    Score: 3.37
    Why:
      • genre match: pop (+2.0)
      • energy 0.90 vs target 0.80 (+0.90)
      • prefers non-acoustic: acousticness 0.06 (+0.47)

#3  Gym Hero — Max Pulse
    Score: 3.35
    Why:
      • genre match: pop (+2.0)
      • energy 0.93 vs target 0.80 (+0.87)
      • prefers non-acoustic: acousticness 0.05 (+0.47)

#4  Rooftop Lights — Indigo Parade
    Score: 2.29
    Why:
      • mood match: happy (+1.0)
      • energy 0.76 vs target 0.80 (+0.96)
      • prefers non-acoustic: acousticness 0.35 (+0.33)

#5  Golden Hour — Indigo Parade
    Score: 2.21
    Why:
      • mood match: happy (+1.0)
      • energy 0.71 vs target 0.80 (+0.91)
      • prefers non-acoustic: acousticness 0.40 (+0.30)
```


---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



