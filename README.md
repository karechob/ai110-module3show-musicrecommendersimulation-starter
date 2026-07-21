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

Output from `python -m src.main` for the default **pop / happy / energy 0.8 / non-acoustic** profile:

```
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

## System Evaluation: Multiple User Profiles

I tested the recommender against three distinct "normal" profiles plus three
adversarial / edge-case profiles designed to try to trick the scoring logic.
All output is from `python -m src.evaluate`.

### Normal profiles

**High-Energy Pop** — `pop / happy / energy 0.9 / non-acoustic`

```
#1  Sunrise City — Neon Echo        Score: 4.33  (genre+mood+energy+acoustic)
#2  Power Sprint — Max Pulse        Score: 3.47  (genre, energy 0.90≈0.90)
#3  Gym Hero — Max Pulse            Score: 3.44  (genre, energy 0.93≈0.90)
#4  Rooftop Lights — Indigo Parade  Score: 2.19  (mood only)
#5  Golden Hour — Indigo Parade     Score: 2.11  (mood only)
```

**Chill Lofi** — `lofi / chill / energy 0.35 / acoustic`

```
#1  Library Rain — Paper Lanterns   Score: 4.43  (genre+mood+energy 0.35≈0.35+acoustic)
#2  Rainy Window — Paper Lanterns   Score: 4.42  (genre+mood+energy+acoustic)
#3  Midnight Coding — LoRoom        Score: 4.29  (genre+mood+energy+acoustic)
#4  Deep Focus — LoRoom             Score: 3.38  (genre+energy, mood=focused misses)
#5  Focus Flow — LoRoom             Score: 3.34  (genre+energy, mood=focused misses)
```

**Deep Intense Rock** — `rock / intense / energy 0.95 / non-acoustic`

```
#1  Thunder Alley — Voltline        Score: 4.46  (genre+mood+energy 0.95≈0.95+acoustic)
#2  Storm Runner — Voltline         Score: 4.41  (genre+mood+energy+acoustic)
#3  Gym Hero — Max Pulse            Score: 2.46  (mood only — pop, not rock)
#4  Power Sprint — Max Pulse        Score: 2.42  (mood only — pop, not rock)
#5  Sunrise City — Neon Echo        Score: 1.28  (no category match)
```

### Adversarial / edge-case profiles

**Conflicting: High-Energy Acoustic Lofi** — `lofi / intense / energy 0.9 / acoustic`
Lofi is calm and low-energy, so asking for *high-energy intense acoustic lofi* is
self-contradictory. Result: the genre bonus (+2.0) dominates and it returns the
lofi catalog anyway, with near-identical low scores (~2.87–2.89) because every
lofi song loses ~0.5 on the energy mismatch. The system does **not** flag the
contradiction — it just quietly ranks lofi songs it "shouldn't" love.

```
#1  Focus Flow — LoRoom             Score: 2.89
#2  Deep Focus — LoRoom             Score: 2.89
#3  Library Rain — Paper Lanterns   Score: 2.88
#4  Midnight Coding — LoRoom        Score: 2.88
#5  Rainy Window — Paper Lanterns   Score: 2.87
```

**Nonexistent: Reggae + Sad** — `reggae / sad / energy 0.5 / non-acoustic`
No song has genre `reggae` or mood `sad`, so those rules can never fire. The
system degrades gracefully to the two continuous rules only (energy closeness +
acoustic fit), producing low scores (~1.1) with **no crash** — but it still
confidently returns 5 songs that match nothing the user actually asked for.

```
#1  Night Drive Loop — Neon Echo    Score: 1.14  (energy 0.75≈0.50 + non-acoustic)
#2  Neon Nights — Neon Echo         Score: 1.12
#3  Sunrise City — Neon Echo        Score: 1.09
#4  Golden Hour — Indigo Parade     Score: 1.09
#5  Power Sprint — Max Pulse        Score: 1.07
```

**Impossible: Calm Acoustic Rock** — `rock / relaxed / energy 0.1 / acoustic`
Rock is loud and non-acoustic, but this user wants *calm acoustic rock*. Here the
scoring logic gets genuinely "tricked": the #1 result is **Slow Tide (ambient)**,
which isn't rock at all — it wins on mood+energy+acoustic (2.33). The real rock
songs (Storm Runner, Thunder Alley) get the +2.0 genre bonus but are punished so
hard on energy and acousticness that they barely tie a non-rock song.

```
#1  Slow Tide — Orbit Bloom         Score: 2.33  (ambient! mood+energy+acoustic)
#2  Storm Runner — Voltline         Score: 2.24  (rock genre, but energy/acoustic tank it)
#3  Thunder Alley — Voltline        Score: 2.19  (rock genre, same problem)
#4  Coffee Shop Stories — Slow Stereo Score: 2.17
#5  Velvet Lounge — Slow Stereo     Score: 2.11
```

### What the edge cases revealed

- **The genre weight can be overpowered.** When a user's continuous preferences
  fight their genre choice (Calm Acoustic Rock), a +2.0 genre match can lose to a
  non-genre song that nails mood + energy + acousticness. Whether that's a bug or
  a feature is a design judgment call.
- **No validation of preferences.** Unknown genres/moods ("reggae", "sad") don't
  error — they silently score 0 on those rules, so the system always returns 5
  songs even when it matches nothing meaningful.
- **No contradiction awareness.** The recommender never tells the user their
  request is impossible; it just returns the least-bad options with low scores.

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



