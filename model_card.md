# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The clearest weakness I discovered during testing is an **"energy gap" bias** created by
the interaction between my scoring rule and the dataset. The catalog's energy values are
bimodal — 9 songs cluster between 0.24 and 0.42 and 9 songs cluster between 0.71 and 0.95,
with no songs at all in the 0.42–0.71 middle range. Because my energy rule awards points
based on `1 - abs(song_energy - target_energy)`, a user with a moderate preference like
`target_energy = 0.55` is far from *every* song and can never earn the near-perfect energy
score that a low-energy (lofi) or high-energy (rock) listener gets automatically. Worse,
that user's energy scores are nearly identical across all songs, so the energy rule stops
distinguishing between songs entirely and the ranking collapses onto genre and mood alone.
In effect the system quietly serves listeners at the two energy extremes well while giving
moderate-energy users flat, undifferentiated recommendations — an unfairness that comes
from the data distribution, not from anything the user did.

A related bias is **genre imbalance**: lofi makes up 5 of 18 songs (~28%) while rock, jazz,
ambient, synthwave, and indie pop have only 2 each, so lofi fans receive a full page of
on-genre results while fans of sparse genres run out after two songs and get filled in with
off-genre tracks. Combined with exact-match genre scoring — which never surfaces musically
adjacent genres like indie pop for a pop fan — the system tends to create a **filter bubble**
that echoes a user's stated taste back rather than broadening it.

---

## 7. Evaluation  

I checked the recommender by running it against six user profiles (see
`src/evaluate.py`) and reading the top-5 list for each. Three were "normal" tastes and
three were tricky edge cases meant to try to break the scoring:

- **High-Energy Pop** — pop, happy, energy 0.9, non-acoustic
- **Chill Lofi** — lofi, chill, energy 0.35, acoustic
- **Deep Intense Rock** — rock, intense, energy 0.95, non-acoustic
- **Conflicting** — lofi but high-energy, intense, acoustic (a contradiction)
- **Nonexistent** — genre "reggae" and mood "sad" (neither exists in the catalog)
- **Impossible** — rock but calm, relaxed, acoustic (rock is none of those)

**What I looked for:** whether songs that truly matched a profile rose to the top, and
whether the explanations made sense.

**What surprised me:** how often songs the user didn't really ask for still crept into the
list. The biggest surprise was the "Impossible" profile — a person who says they want calm,
acoustic rock gets an **ambient** song (*Slow Tide*) as their #1 pick, beating actual rock
songs, because the calm-and-acoustic parts of their request outweighed the genre. It made me
realize the recommender never says "that request doesn't really exist" — it just returns the
least-bad option and sounds confident about it.

### Comparing the profiles (what changed, and why it makes sense)

- **High-Energy Pop vs Chill Lofi:** These are near-opposites and the output flips
  completely — Pop returns loud, upbeat tracks (Sunrise City, Power Sprint) while Lofi returns
  quiet, acoustic ones (Library Rain, Rainy Window). This is exactly what should happen: they
  disagree on genre, mood, *and* energy, so almost no song scores well for both.
- **High-Energy Pop vs Deep Intense Rock:** Both want high energy, so the *energy* part of
  their lists looks similar — but the top spots differ because genre wins first. Rock pulls
  Thunder Alley and Storm Runner to the top; Pop pulls Sunrise City and the Max Pulse tracks.
  It makes sense because energy alone can't override a genre match.
- **Chill Lofi vs Deep Intense Rock:** Complete opposites on every axis, so there is zero
  overlap in their top 5 — the clearest sign the profiles are really testing different things.
- **Conflicting vs Nonexistent (edge cases):** Both return low scores, but for different
  reasons — the Conflicting profile still gets its lofi genre bonus (~2.8), while the
  Nonexistent profile matches no genre or mood at all and scrapes by on energy alone (~1.1).
  This shows the genre weight is doing a lot of the heavy lifting.

**The "Gym Hero" question, in plain language:** Someone asks for *Happy Pop*, and the
workout track *Gym Hero* keeps showing up even though its mood is "intense," not "happy." Why?
Think of scoring like awarding points. *Gym Hero* is genuinely pop, so it earns the big genre
prize (+2 points). It's also very high-energy, which is close to what a happy-pop fan usually
wants, so it earns almost a full energy point too. It misses the "happy mood" point — but the
two points it *did* win are enough to push it above songs that have the right mood but the
wrong genre. In short, the song is winning on the categories that count for the most, even
though it "feels" a little off — which is a good example of how the weights I chose shape the
results.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
