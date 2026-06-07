# DJ's Dungeon Crawl

A D&D-style terminal dungeon crawler written in Python, inspired by the old-school MUDs of the x286 era. Navigate a procedurally generated dungeon, battle monsters, find treasure, and visit the merchant — how deep can you go?

## Requirements

- Python 3.6+
- A color terminal (Terminal.app, iTerm2, xterm, etc.)

## How to Run

```bash
python3 dungeon-crawl.py
```

Or use the launch script:

```bash
./play.sh
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move / Attack (bump into a monster) |
| `ENTER` | Descend stairs (`>`) |
| `p` | Drink a potion (restores full HP) |
| `i` | Inventory |
| `?` | Help |
| `q` / `ESC` | Quit |

## Map Legend

| Symbol | Meaning |
|--------|---------|
| `@` | You |
| `#` | Wall |
| `.` | Floor |
| `+` | Door |
| `>` | Stairs down |
| `$` | Gold pile or Shopkeeper |
| `*` | Treasure chest (gold + item) |
| `!` | Health Potion (walk over to use) |

## Monsters

| Symbol | Monster | Difficulty |
|--------|---------|------------|
| `r` | Giant Rat | Easy |
| `k` | Kobold | Easy |
| `g` | Goblin | Easy |
| `o` | Orc | Moderate |
| `s` | Skeleton | Moderate |
| `z` | Zombie | Moderate |
| `h` | Hobgoblin | Moderate |
| `T` | Troll | Hard |
| `O` | Ogre | Hard |
| `E` | Dark Elf | Hard |
| `M` | Minotaur | Hard |
| `V` | Vampire | Very Hard |
| `W` | Wyvern | Very Hard |
| `L` | Lich | Very Hard |
| `G` | Stone Golem | Very Hard |
| `D` | Dragon | Deadly |
| `K` | Death Knight | Deadly |
| `B` | Balrog | Deadly |

## Weapons

| Weapon | ATK | Cost |
|--------|-----|------|
| Rusty Dagger | +2 | Starting weapon |
| Short Sword | +5 | 50 gp |
| Long Sword | +9 | 150 gp |
| Battle Axe | +14 | 300 gp |
| War Hammer | +18 | 500 gp |
| Enchanted Blade | +24 | 1,000 gp |
| Dragon Slayer | +32 | 2,000 gp |
| Excalibur | +45 | 5,000 gp |

## Armor

| Armor | DEF | Cost |
|-------|-----|------|
| Tattered Robe | +0 | Starting armor |
| Leather Armor | +3 | 60 gp |
| Chain Mail | +7 | 200 gp |
| Scale Armor | +12 | 400 gp |
| Plate Mail | +18 | 800 gp |
| Dragon Scale | +24 | 1,500 gp |
| Mithril Plate | +32 | 3,000 gp |
| Celestial Armor | +45 | 6,000 gp |

## Gameplay Tips

- **Bump into monsters** to attack them — no attack key needed.
- **Health Potions** (`!`) on the floor restore full HP instantly when walked over.
- **Shopkeepers** (`$`, shown in cyan) appear on every level — buy better gear as you find gold.
- **Treasure chests** (`*`) contain gold and sometimes a weapon, armor, or potion. Better items are auto-equipped if they're stronger than what you're wearing.
- **Descend the stairs** (`>`) to reach deeper levels. Monsters scale in strength with dungeon depth.
- **Level up** by defeating monsters — each level grants +12 max HP, +2 ATK, and +1 DEF.
- Watch your HP bar color: **green** = healthy, **yellow** = wounded, **red** = critical.

## Author

Doug Johnson — doug@tinydragonsolutions.com
