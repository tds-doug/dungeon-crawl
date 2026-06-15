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
| `F` | Fairy (golden — walk into for +100 gold and full health) |

## Fairy

A golden `F` appears once per level and **flies around randomly for 200 moves** before vanishing. Walk into it to receive **+100 gold and full health**. You'll get a hint when you enter a level that has one.

## Allies

Allies appear in **yellow** on the floor. Walk over one to pick it up — it will follow you for **50 moves**, then depart. Only one of each type spawns per floor.

| Symbol | Ally | Behavior |
|--------|------|----------|
| `e` | Elf Archer | Fires at the nearest monster within **5 tiles** each turn |
| `d` | Dwarf Warrior | Strikes alongside you every time you attack |
| `R` | Ranger | Fires at the nearest monster within **8 tiles** each turn (longer range, hits harder than the Elf) |
| `Z` | Wizard | Blasts **every** monster within 3 tiles with AOE magic each turn |

## Monsters

All monsters appear in **red**. Deeper floors spawn tougher enemies.

| Symbol | Monster | Difficulty | First Appears |
|--------|---------|------------|---------------|
| `r` | Giant Rat | Easy | Depth 1 |
| `k` | Kobold | Easy | Depth 1 |
| `g` | Goblin | Easy | Depth 1 |
| `o` | Orc | Moderate | Depth 2 |
| `s` | Skeleton | Moderate | Depth 2 |
| `z` | Zombie | Moderate | Depth 3 |
| `h` | Hobgoblin | Moderate | Depth 3 |
| `T` | Troll | Hard | Depth 4 |
| `O` | Ogre | Hard | Depth 4 |
| `E` | Dark Elf | Hard | Depth 5 |
| `M` | Minotaur | Hard | Depth 5 |
| `w` | Werewolf | Hard | Depth 5 |
| `V` | Vampire | Very Hard | Depth 6 |
| `W` | Wyvern | Very Hard | Depth 6 |
| `C` | Cyclops | Very Hard | Depth 6 |
| `L` | Lich | Very Hard | Depth 7 |
| `G` | Stone Golem | Very Hard | Depth 7 |
| `D` | Dragon | Deadly | Depth 8 |
| `N` | Necromancer | Deadly | Depth 8 |
| `K` | Death Knight | Deadly | Depth 9 |
| `B` | Balrog | Deadly | Depth 10 |

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
- **The Fairy** (`F`, golden) appears once per level and drifts around for 200 moves — intercept it for +100 gold and a full heal.
- **Allies** (`e`, `d`, `R`, `Z`) appear on each floor — walk over them to recruit them. They act automatically and last 50 moves. The Wizard's AOE and the Ranger's long range make tight corridors much safer.
- **Health Potions** (`!`) on the floor restore full HP instantly when walked over.
- **Shopkeepers** (`$`, shown in cyan) appear on every level — buy better gear as you find gold.
- **Treasure chests** (`*`) contain gold and sometimes a weapon, armor, or potion. Better items are auto-equipped if they're stronger than what you're wearing.
- **Descend the stairs** (`>`) to reach deeper levels. Monsters scale in strength with dungeon depth.
- **Level up** by defeating monsters — each level grants +12 max HP, +2 ATK, and +1 DEF.
- Watch your HP bar color: **green** = healthy, **yellow** = wounded, **red** = critical.

## Author

Doug Johnson — doug@tinydragonsolutions.com
