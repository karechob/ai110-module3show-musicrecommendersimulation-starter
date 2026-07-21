# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Real-world recommenders like Spotify and YouTube predict what you'll enjoy next using two main ideas: collaborative filtering, which learns from the behavior of millions of users ("people who liked what you like also liked this") to capture taste that's hard to describe but needs lots of listening data, and content-based filtering, which looks at the measurable attributes of each song and recommends ones whose attributes match your preferences — which is how a brand-new track can be suggested before anyone has played it. My version is a small content-based recommender, because I have a song catalog but no user listening history, so I score each song by how well its features match a user's taste profile; each Song uses its genre, mood, energy, and acousticness for scoring (with id, title, and artist only for display, and tempo_bpm, valence, and danceability reserved for later experiments), and each UserProfile mirrors these with favorite_genre, favorite_mood, target_energy, and likes_acoustic. It prioritizes genre first as the strongest signal of taste, then mood, then how close a song's energy is to the user's target (rewarding closeness rather than just higher values), and finally whether its acousticness fits — producing recommendations that are transparent and easy to explain, at the cost of the surprising discoveries that collaborative filtering provides.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



