# Roadmap

# OmniToon : ToonTown AI

---

## Purpose

Teach Python how to play ToonTown by utilizing object-orient programming (OOP), design patterns, machine learning (ML), and computer vision. Ultimately, I want to learn how to properly implement and optimize machine learning algorithms when given large amounts of data while also maintaining best practices in Python, OOP, and design patterns.

## Use Cases

OmniToon(s) wandering around ToonTown supporting other players (or other OmniToons) in...

1. Training Gags
2. Completing tasks
3. Conquering buildings

---

## Roadmap

### Battles

- Select random Gag
- Choose random target Cog(s)
- Don't use Sound on Lured Cogs (unless maximizing rewards while training Sound or Lure)
- Heal other Toons if they're low Laff Points

### Interface Python with ToonTown

- Move the OmniToon
- Classify Cogs
- Start a Battle
    - Read the Gag menu
    - Choose Gag and target Cog(s)
- Pass/Run from Battle
- Re-supply Gags from the Gag Shop
- Locate [Treasures](https://toontown.fandom.com/wiki/Treasure) (health packs) in Playgrounds
- Switch servers if there's a desired/unwanted invasion

### Battle Parser

- Parse Battle data (Cogs, Toons, attacks, Gags used, Gags available, etc.)
- Collect large amounts of data by running Battle simulations
    - Feed data into ML algorithms
    - Determine most optimal Gags to use when running various strategies

### Fishing

- Catch fish, turn them in, get Jellybeans for more Gags

### Battles (Strategy design pattern)

- Maximize total Battle rewards
    - Watch [invasion tracker](https://toonhq.org/invasions/) and switch servers
- Defeat Cogs ASAP (for tasks)
    - Learn to stack Gags (everyone uses Lure, Throw, Squirt, etc.)
- Train specific Gags
    - Learn Trap/Lure combos
    - Don't use Sound on Lured Cogs
- Support other Toons (prioritize Toon-Up, Trap, Lure, etc)

### Tasks

- Optimize movement in order to complete tasks as fast as possible
    - Learn ToonTown's neighborhoods, playgrounds, and streets
- Select tasks that are most similar in order to knock out multiple tasks at once