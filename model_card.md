# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

A simple recommender that matches songs to your vibe.

---

## 2. Intended Use  

**What it is for:** VibeFinder suggests songs from a small catalog. You give it a taste
profile (a genre, a mood, an energy level, and whether you like acoustic music). It gives you
back the 5 songs that best fit.

**Who it is for:** This is a classroom project for learning. It is not a real product.

**Assumptions it makes:** It assumes you can describe your taste with one genre and one mood.
It assumes the songs in the catalog are the only songs that exist.

**What it should NOT be used for:** It should not be used to make real music suggestions for
real people. It is too small and too simple for that. It should not be used to judge what
"good" music is, or to decide what anyone should listen to.

---

## 3. How the Model Works  

Think of it like a points game. Every song starts with zero points. Then the model checks
the song against your taste profile and hands out points:

- **+2 points** if the song's genre matches your favorite genre.
- **+1 point** if the song's mood matches your favorite mood.
- **Up to +1 point** for energy — a full point if the song's energy is exactly what you want,
  and fewer points the further it drifts from your target (too high loses points, too low
  loses points).
- **Up to +0.5 points** for acoustic fit — more points if the song matches whether you like
  acoustic music or not.

The model adds up the points for every song, then sorts them from most points to fewest and
shows you the top 5. It also lists the reasons each song scored, so you can see *why* it was
picked. Genre is worth the most points on purpose, because genre is the strongest clue about
what someone likes.

I built this out from the starter code, which only returned the first few songs without
scoring them at all.

---

## 4. Data  

The catalog has **18 songs**. I started with 10 and added 8 more.

Each song has these details: title, artist, genre, mood, energy, tempo, valence,
danceability, and acousticness. The model only uses genre, mood, energy, and acousticness to
score. The rest are saved for later.

**Genres:** pop, lofi, rock, ambient, jazz, synthwave, and indie pop.
**Moods:** happy, chill, intense, relaxed, moody, and focused.

**What is missing:** The catalog is tiny. Many real genres are not here at all (no hip-hop,
country, classical, or metal). There are no lyrics and no language info. Lofi has the most
songs, so the data is not balanced across genres.

---

## 5. Strengths  

The system works well for clear, common tastes. If you ask for happy pop, chill lofi, or
intense rock, it gives sensible picks that match on genre, mood, and energy.

It captures the idea that *closeness* matters for energy — it does not just grab the loudest
song, it grabs songs near the energy you asked for.

Every recommendation comes with reasons, so it is easy to understand why a song showed up.
This made testing simple, because I could always see what the model was "thinking."

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

If I kept building this, I would change three things:

1. **Fix the energy scoring.** Right now moderate-energy users get flat results. I would score
   energy based on the songs that actually exist, so everyone gets useful picks.
2. **Let similar genres count.** A pop fan should sometimes see indie pop. I would give partial
   points for genres that are close, instead of only exact matches.
3. **Add bigger, more balanced data.** More songs across more genres would make the picks feel
   less repetitive and less biased toward lofi.

---

## 9. Personal Reflection  

**Biggest learning moment:** Realizing a recommender is just a scoring rule plus a sort. Once I
saw that a "recommendation" is only points added up and put in order, the whole thing stopped
feeling like magic and started feeling like something I could build and change myself.

**How AI tools helped, and when I checked them:** I used an AI assistant to design the scoring
math, explain closeness scoring, and format the output. It was fastest when I asked clear,
specific questions. But I still had to double-check its work — I verified the loaded data were
real numbers, ran the code myself, and read the actual output for each profile to confirm the
picks made sense. The AI could suggest a plan, but I had to prove it was true.

**What surprised me:** How real the results feel from such a simple rule. Four point-based checks
were enough to make the picks feel like a person chose them, even though it is only arithmetic.
That is also a little unsettling — "feels smart" and "is smart" are not the same thing.

**What I would try next:** Fix the energy-gap bias, give partial credit for similar genres, and
add a bigger, more balanced catalog so the picks feel fresh instead of repetitive.

The project changed how I see apps like Spotify. When a song "just fits," it is not magic — it is
math, weights, and data, and those choices quietly decide what I do and do not get to hear.
