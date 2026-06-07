#!/usr/bin/env python3
# ==============================================================================
# Script Name: dungeon-crawl.py
# Author: Doug Johnson - doug@tinydragonsolutions.com
# Description: This script is designed to recreate an old style dungeon crawl that
#		was run on ancient computer hardware you cannot even find anymore.
#
# Version History:
# ------------------------------------------------------------------------------
# 1.0.0 - Initial release.
# 2.0.0 - Added potions to restore health.
#
# Prerequisites:
#
# Usage:
#   python3 dungeon-crawl.py
#
# Disclaimer: This script is provided as-is, and the author assumes no liability
# for any issues arising from its execution. Ensure all system requirements are met
# before running this script.
# ============================================================================== 

"""
DungeonCrawl — An Old Style Terminal MUD
Controls: Arrow Keys=Move/Attack  ENTER=Stairs  p=Potion  i=Inventory  ?=Help  q=Quit
"""

import curses
import random
import sys
from typing import List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════
#  MAP CONSTANTS
# ═══════════════════════════════════════════════════════════════════

MAP_W     = 100
MAP_H     = 55
MAX_ROOMS = 20
ROOM_MIN  = 5
ROOM_MAX  = 14

# Tile IDs
WALL  = 0
FLOOR = 1
DOOR  = 2
DOWN  = 3   # stairs down

TILE_CH = {WALL: '#', FLOOR: '.', DOOR: '+', DOWN: '>'}

# ═══════════════════════════════════════════════════════════════════
#  COLOR PAIR IDs
# ═══════════════════════════════════════════════════════════════════

CP_DEFAULT  = 1   # white / default
CP_PLAYER   = 2   # bright yellow  — @
CP_WALL     = 3   # dim white      — #
CP_FLOOR    = 4   # dark           — .
CP_MON_R    = 5   # red monsters
CP_TREASURE = 6   # yellow treasure
CP_SHOP     = 7   # cyan shopkeeper
CP_STAIR    = 8   # magenta stairs
CP_TITLE    = 9   # bold white
CP_STAT     = 10  # green stats
CP_MSG_GOOD = 11  # green messages
CP_MSG_BAD  = 12  # red messages
CP_MSG_INFO = 13  # cyan messages
CP_DOOR     = 14  # yellow door
CP_SELECT   = 15  # black on white (menu)
CP_MON_G    = 16  # green monsters
CP_MON_Y    = 17  # yellow monsters
CP_MON_W    = 18  # white monsters
CP_MON_C    = 19  # cyan monsters
CP_HP_HIGH  = 20  # green HP
CP_HP_MED   = 21  # yellow HP
CP_HP_LOW   = 22  # red HP

# ═══════════════════════════════════════════════════════════════════
#  ITEM TABLES
# ═══════════════════════════════════════════════════════════════════

WEAPONS = [
    dict(name="Rusty Dagger",     atk=2,  cost=0,    tier=0),
    dict(name="Short Sword",      atk=5,  cost=50,   tier=1),
    dict(name="Long Sword",       atk=9,  cost=150,  tier=2),
    dict(name="Battle Axe",       atk=14, cost=300,  tier=3),
    dict(name="War Hammer",       atk=18, cost=500,  tier=4),
    dict(name="Enchanted Blade",  atk=24, cost=1000, tier=5),
    dict(name="Dragon Slayer",    atk=32, cost=2000, tier=6),
    dict(name="Excalibur",        atk=45, cost=5000, tier=7),
]

ARMORS = [
    dict(name="Tattered Robe",    arm=0,  cost=0,    tier=0),
    dict(name="Leather Armor",    arm=3,  cost=60,   tier=1),
    dict(name="Chain Mail",       arm=7,  cost=200,  tier=2),
    dict(name="Scale Armor",      arm=12, cost=400,  tier=3),
    dict(name="Plate Mail",       arm=18, cost=800,  tier=4),
    dict(name="Dragon Scale",     arm=24, cost=1500, tier=5),
    dict(name="Mithril Plate",    arm=32, cost=3000, tier=6),
    dict(name="Celestial Armor",  arm=45, cost=6000, tier=7),
]

POTIONS = [
    dict(name="Minor Potion",     hp=20,  cost=30),
    dict(name="Healing Potion",   hp=50,  cost=80),
    dict(name="Greater Potion",   hp=100, cost=200),
]

# ═══════════════════════════════════════════════════════════════════
#  MONSTER TEMPLATES
#  col: r=red g=green y=yellow w=white c=cyan m=magenta
# ═══════════════════════════════════════════════════════════════════

MONSTERS = [
    dict(name="Giant Rat",   ch="r", col="y", hp=5,   atk=2,  arm=0,  xp=6,   gold=(0,3),    min_d=1),
    dict(name="Kobold",      ch="k", col="g", hp=7,   atk=3,  arm=0,  xp=8,   gold=(1,4),    min_d=1),
    dict(name="Goblin",      ch="g", col="g", hp=10,  atk=4,  arm=1,  xp=12,  gold=(2,7),    min_d=1),
    dict(name="Orc",         ch="o", col="y", hp=18,  atk=7,  arm=2,  xp=22,  gold=(4,12),   min_d=2),
    dict(name="Skeleton",    ch="s", col="w", hp=14,  atk=6,  arm=3,  xp=18,  gold=(2,8),    min_d=2),
    dict(name="Zombie",      ch="z", col="g", hp=22,  atk=8,  arm=2,  xp=26,  gold=(3,10),   min_d=3),
    dict(name="Hobgoblin",   ch="h", col="r", hp=24,  atk=9,  arm=3,  xp=32,  gold=(5,16),   min_d=3),
    dict(name="Troll",       ch="T", col="g", hp=38,  atk=12, arm=5,  xp=52,  gold=(8,22),   min_d=4),
    dict(name="Ogre",        ch="O", col="r", hp=42,  atk=14, arm=4,  xp=62,  gold=(10,26),  min_d=4),
    dict(name="Dark Elf",    ch="E", col="c", hp=30,  atk=15, arm=6,  xp=58,  gold=(10,32),  min_d=5),
    dict(name="Minotaur",    ch="M", col="y", hp=50,  atk=16, arm=7,  xp=75,  gold=(12,35),  min_d=5),
    dict(name="Vampire",     ch="V", col="r", hp=48,  atk=18, arm=8,  xp=90,  gold=(15,45),  min_d=6),
    dict(name="Wyvern",      ch="W", col="y", hp=60,  atk=20, arm=9,  xp=110, gold=(18,50),  min_d=6),
    dict(name="Lich",        ch="L", col="c", hp=58,  atk=22, arm=10, xp=130, gold=(20,65),  min_d=7),
    dict(name="Stone Golem", ch="G", col="w", hp=80,  atk=18, arm=15, xp=150, gold=(15,55),  min_d=7),
    dict(name="Dragon",      ch="D", col="r", hp=90,  atk=28, arm=14, xp=220, gold=(35,90),  min_d=8),
    dict(name="Death Knight", ch="K", col="c", hp=100, atk=30, arm=16, xp=280, gold=(40,100), min_d=9),
    dict(name="Balrog",      ch="B", col="r", hp=120, atk=35, arm=18, xp=350, gold=(60,140), min_d=10),
]

# ═══════════════════════════════════════════════════════════════════
#  DATA CLASSES
# ═══════════════════════════════════════════════════════════════════

class Room:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def cx(self) -> int:
        return self.x + self.w // 2

    @property
    def cy(self) -> int:
        return self.y + self.h // 2

    def intersects(self, other: "Room") -> bool:
        return (self.x < other.x + other.w + 1 and self.x + self.w + 1 > other.x and
                self.y < other.y + other.h + 1 and self.y + self.h + 1 > other.y)

    def random_inner(self) -> Tuple[int, int]:
        return (random.randint(self.x + 1, self.x + self.w - 2),
                random.randint(self.y + 1, self.y + self.h - 2))


class Monster:
    def __init__(self, tmpl: dict, x: int, y: int, depth: int):
        scale = 1.0 + (depth - 1) * 0.18
        self.name   = tmpl["name"]
        self.ch     = tmpl["ch"]
        self.col    = tmpl["col"]
        self.x      = x
        self.y      = y
        self.max_hp = max(1, int(tmpl["hp"] * scale))
        self.hp     = self.max_hp
        self.atk    = max(1, int(tmpl["atk"] * scale))
        self.arm    = max(0, int(tmpl["arm"] * scale))
        self.xp     = max(1, int(tmpl["xp"] * scale))
        self._gold  = tmpl["gold"]

    def alive(self) -> bool:
        return self.hp > 0

    def take_hit(self, raw: int) -> int:
        dmg = max(1, raw - self.arm // 2)
        self.hp -= dmg
        return dmg

    def loot_gold(self) -> int:
        lo, hi = self._gold
        return random.randint(lo, hi)


class Treasure:
    def __init__(self, x: int, y: int, gold: int,
                 item: Optional[dict] = None, itype: str = ""):
        self.x, self.y = x, y
        self.gold       = gold
        self.item       = item
        self.itype      = itype   # "weapon" | "armor" | "potion"


class Shopkeeper:
    def __init__(self, x: int, y: int, depth: int):
        self.x, self.y = x, y
        self.stock: List[dict] = self._build(depth)

    def _build(self, depth: int) -> List[dict]:
        stock = []
        max_w = min(depth // 2 + 2, len(WEAPONS) - 1)
        for w in WEAPONS[1 : max_w + 1]:
            stock.append({**w, "itype": "weapon"})
        max_a = min(depth // 2 + 2, len(ARMORS) - 1)
        for a in ARMORS[1 : max_a + 1]:
            stock.append({**a, "itype": "armor"})
        for p in POTIONS:
            stock.append({**p, "itype": "potion"})
        return stock


class Ally:
    """A companion that follows the player for up to 50 moves."""
    TYPES = {
        "elf":   dict(name="Elf Archer",   ch="e", col="g"),
        "dwarf": dict(name="Dwarf Warrior", ch="d", col="y"),
    }

    def __init__(self, atype: str, x: int, y: int):
        info        = self.TYPES[atype]
        self.atype  = atype
        self.name   = info["name"]
        self.ch     = info["ch"]
        self.col    = info["col"]
        self.x      = x
        self.y      = y
        self.moves_left = 50

    def alive(self) -> bool:
        return self.moves_left > 0

    def atk_roll(self, player_level: int) -> int:
        base = 4 + player_level * 2 if self.atype == "elf" else 3 + player_level * 2
        return base + random.randint(0, 3)


class Player:
    def __init__(self):
        self.x         = 0
        self.y         = 0
        self.level     = 1
        self.xp        = 0
        self.xp_next   = 100
        self.max_hp    = 30
        self.hp        = 30
        self.base_atk  = 4
        self.base_arm  = 1
        self.gold      = 50
        self.weapon    = WEAPONS[0].copy()
        self.armor     = ARMORS[0].copy()
        self.potions: List[dict] = []
        self.allies:  List[Ally] = []
        self.kills     = 0
        self.depth     = 1

    @property
    def atk(self) -> int:
        return self.base_atk + self.weapon["atk"]

    @property
    def arm(self) -> int:
        return self.base_arm + self.armor["arm"]

    def alive(self) -> bool:
        return self.hp > 0

    def hit_monster(self, m: Monster) -> int:
        raw = self.atk + random.randint(-2, 3)
        return m.take_hit(raw)

    def take_hit(self, m: Monster) -> int:
        raw = m.atk + random.randint(-1, 2)
        dmg = max(1, raw - self.arm // 2)
        self.hp -= dmg
        return dmg

    def gain_xp(self, amount: int) -> bool:
        """Returns True if leveled up."""
        self.xp += amount
        if self.xp >= self.xp_next:
            self.xp      -= self.xp_next
            self.xp_next  = int(self.xp_next * 1.65)
            self.level   += 1
            self.max_hp  += 12
            self.hp       = min(self.hp + 12, self.max_hp)
            self.base_atk += 2
            self.base_arm += 1
            return True
        return False

    def drink_potion(self) -> Optional[str]:
        if not self.potions:
            return None
        pot = self.potions.pop(0)
        self.hp = self.max_hp
        return f"You drink a {pot['name']}! HP fully restored!"


# ═══════════════════════════════════════════════════════════════════
#  DUNGEON LEVEL
# ═══════════════════════════════════════════════════════════════════

class DungeonLevel:
    def __init__(self, depth: int, player: Player):
        self.depth     = depth
        self.tiles     = [[WALL] * MAP_W for _ in range(MAP_H)]
        self.rooms: List[Room]           = []
        self.monsters: List[Monster]     = []
        self.treasures: List[Treasure]   = []
        self.floor_potions: List[Tuple[int, int]] = []
        self.floor_allies:  List[Ally]           = []
        self.shopkeeper: Optional[Shopkeeper] = None
        self.stair_x   = 0
        self.stair_y   = 0
        self.entry_x   = 0
        self.entry_y   = 0
        self._generate(player)

    # ── Map carving ───────────────────────────────────────────

    def _carve_room(self, r: Room):
        for y in range(r.y, r.y + r.h):
            for x in range(r.x, r.x + r.w):
                self.tiles[y][x] = FLOOR

    def _htunnel(self, x1: int, x2: int, y: int):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 < x < MAP_W and 0 < y < MAP_H:
                self.tiles[y][x] = FLOOR

    def _vtunnel(self, y1: int, y2: int, x: int):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 < x < MAP_W and 0 < y < MAP_H:
                self.tiles[y][x] = FLOOR

    # ── Population ────────────────────────────────────────────

    def _place_monsters(self, room: Room, depth: int):
        count = random.randint(1, min(4, 1 + depth // 2))
        valid = [m for m in MONSTERS if m["min_d"] <= depth]
        if not valid:
            valid = MONSTERS[:3]
        # Weight: common monsters appear more often
        weights = [1.0 / max(1, depth - m["min_d"] + 1) for m in valid]
        total = sum(weights)
        weights = [w / total for w in weights]
        for _ in range(count):
            for _attempt in range(20):
                mx, my = room.random_inner()
                if (self.tiles[my][mx] == FLOOR and
                        not self.monster_at(mx, my) and
                        (mx, my) != (self.stair_x, self.stair_y)):
                    tmpl = random.choices(valid, weights=weights, k=1)[0]
                    self.monsters.append(Monster(tmpl, mx, my, depth))
                    break

    def _place_treasure(self, room: Room, depth: int):
        for _attempt in range(15):
            tx, ty = room.random_inner()
            if (self.tiles[ty][tx] == FLOOR and
                    not self.treasure_at(tx, ty) and
                    (tx, ty) != (self.stair_x, self.stair_y)):
                gold = random.randint(5 * depth, 18 * depth)
                item, itype = None, ""
                if random.random() < 0.35:
                    if random.random() < 0.45:
                        tier = min(random.randint(0, depth // 2 + 1), len(WEAPONS) - 1)
                        item  = WEAPONS[tier].copy()
                        itype = "weapon"
                    elif random.random() < 0.6:
                        tier = min(random.randint(0, depth // 2 + 1), len(ARMORS) - 1)
                        item  = ARMORS[tier].copy()
                        itype = "armor"
                    else:
                        item  = random.choice(POTIONS).copy()
                        itype = "potion"
                self.treasures.append(Treasure(tx, ty, gold, item, itype))
                return

    # ── Generation ────────────────────────────────────────────

    def _generate(self, player: Player):
        rooms: List[Room] = []
        for _ in range(MAX_ROOMS * 5):
            w = random.randint(ROOM_MIN, ROOM_MAX)
            h = random.randint(ROOM_MIN, ROOM_MAX)
            x = random.randint(1, MAP_W - w - 2)
            y = random.randint(1, MAP_H - h - 2)
            room = Room(x, y, w, h)
            if not any(room.intersects(r) for r in rooms):
                self._carve_room(room)
                if rooms:
                    px, py = rooms[-1].cx, rooms[-1].cy
                    cx, cy = room.cx, room.cy
                    if random.random() < 0.5:
                        self._htunnel(px, cx, py)
                        self._vtunnel(py, cy, cx)
                    else:
                        self._vtunnel(py, cy, px)
                        self._htunnel(px, cx, cy)
                rooms.append(room)
            if len(rooms) >= MAX_ROOMS:
                break

        self.rooms = rooms
        if not rooms:
            return

        # Entry in first room, stairs in last
        self.entry_x, self.entry_y = rooms[0].cx, rooms[0].cy
        self.stair_x, self.stair_y = rooms[-1].cx, rooms[-1].cy
        self.tiles[self.stair_y][self.stair_x] = DOWN

        # Shopkeeper in middle room (not first or last)
        if len(rooms) >= 3:
            idx = len(rooms) // 2
            sx, sy = rooms[idx].random_inner()
            self.shopkeeper = Shopkeeper(sx, sy, self.depth)

        # Populate all rooms except first (spawn) and shop room
        shop_idx = len(rooms) // 2 if len(rooms) >= 3 else -1
        for i, room in enumerate(rooms[1:], 1):
            if i == shop_idx:
                continue
            self._place_monsters(room, self.depth)
            if random.random() < 0.55:
                self._place_treasure(room, self.depth)

        self._place_floor_potions(rooms, shop_idx)
        self._place_allies(rooms, shop_idx)

    def _place_floor_potions(self, rooms: list, shop_idx: int):
        """Scatter health potions across rooms (skip spawn room and shop room)."""
        eligible = [r for i, r in enumerate(rooms) if i != 0 and i != shop_idx]
        random.shuffle(eligible)
        count = min(len(eligible), random.randint(2, 4))
        for room in eligible[:count]:
            for _attempt in range(15):
                px, py = room.random_inner()
                if (self.tiles[py][px] == FLOOR and
                        (px, py) not in self.floor_potions and
                        not self.treasure_at(px, py) and
                        (px, py) != (self.stair_x, self.stair_y)):
                    self.floor_potions.append((px, py))
                    break

    def _place_allies(self, rooms: list, shop_idx: int):
        """Spawn one elf and one dwarf on the floor in separate rooms."""
        eligible = [r for i, r in enumerate(rooms) if i != 0 and i != shop_idx]
        random.shuffle(eligible)
        taken_positions: List[Tuple[int, int]] = []
        for atype, room in zip(("elf", "dwarf"), eligible[:2]):
            for _attempt in range(20):
                ax, ay = room.random_inner()
                if (self.tiles[ay][ax] == FLOOR and
                        (ax, ay) not in self.floor_potions and
                        (ax, ay) not in taken_positions and
                        not self.treasure_at(ax, ay) and
                        not self.monster_at(ax, ay) and
                        (ax, ay) != (self.stair_x, self.stair_y)):
                    self.floor_allies.append(Ally(atype, ax, ay))
                    taken_positions.append((ax, ay))
                    break

    def _ally_at(self, x: int, y: int) -> Optional[Ally]:
        for a in self.floor_allies:
            if a.x == x and a.y == y:
                return a
        return None

    # ── Queries ───────────────────────────────────────────────

    def monster_at(self, x: int, y: int) -> Optional[Monster]:
        for m in self.monsters:
            if m.alive() and m.x == x and m.y == y:
                return m
        return None

    def treasure_at(self, x: int, y: int) -> Optional[Treasure]:
        for t in self.treasures:
            if t.x == x and t.y == y:
                return t
        return None

    def walkable(self, x: int, y: int) -> bool:
        return 0 <= x < MAP_W and 0 <= y < MAP_H and self.tiles[y][x] != WALL


# ═══════════════════════════════════════════════════════════════════
#  GAME
# ═══════════════════════════════════════════════════════════════════

class Game:
    PANEL_W = 26
    MSG_H   = 5

    # Legend entries: (glyph, color_pair, label)
    LEGEND_MAP = [
        ('@', CP_PLAYER,   'You'),
        ('#', CP_WALL,     'Wall'),
        ('.', CP_FLOOR,    'Floor'),
        ('+', CP_DOOR,     'Door'),
        ('>', CP_STAIR,    'Stairs down'),
        ('$', CP_TREASURE, 'Gold / Shop'),
        ('*', CP_TREASURE, 'Item + Gold'),
        ('!', CP_MSG_GOOD, 'Health Potion'),
    ]
    LEGEND_ALLY = [
        ('e', CP_MON_G, 'Elf Archer'),
        ('d', CP_MON_Y, 'Dwarf Warrior'),
    ]
    LEGEND_MON = [
        ('r', CP_MON_Y, 'Giant Rat'),
        ('k', CP_MON_G, 'Kobold'),
        ('g', CP_MON_G, 'Goblin'),
        ('o', CP_MON_Y, 'Orc'),
        ('s', CP_MON_W, 'Skeleton'),
        ('z', CP_MON_G, 'Zombie'),
        ('h', CP_MON_R, 'Hobgoblin'),
        ('T', CP_MON_G, 'Troll'),
        ('O', CP_MON_R, 'Ogre'),
        ('E', CP_MON_C, 'Dark Elf'),
        ('M', CP_MON_Y, 'Minotaur'),
        ('V', CP_MON_R, 'Vampire'),
        ('W', CP_MON_Y, 'Wyvern'),
        ('L', CP_MON_C, 'Lich'),
        ('G', CP_MON_W, 'Stone Golem'),
        ('D', CP_MON_R, 'Dragon'),
        ('K', CP_MON_C, 'Death Knight'),
        ('B', CP_MON_R, 'Balrog'),
    ]

    def __init__(self, scr):
        self.scr      = scr
        self.player   = Player()
        self.level: Optional[DungeonLevel] = None
        self.messages: List[Tuple[str, int]] = []
        self.running  = True
        self._init_colors()
        self._new_level()

    # ── Initialization ────────────────────────────────────────

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        bg = -1
        curses.init_pair(CP_DEFAULT,  curses.COLOR_WHITE,   bg)
        curses.init_pair(CP_PLAYER,   curses.COLOR_YELLOW,  bg)
        curses.init_pair(CP_WALL,     curses.COLOR_WHITE,   bg)
        curses.init_pair(CP_FLOOR,    curses.COLOR_WHITE,   bg)
        curses.init_pair(CP_MON_R,    curses.COLOR_RED,     bg)
        curses.init_pair(CP_TREASURE, curses.COLOR_YELLOW,  bg)
        curses.init_pair(CP_SHOP,     curses.COLOR_CYAN,    bg)
        curses.init_pair(CP_STAIR,    curses.COLOR_MAGENTA, bg)
        curses.init_pair(CP_TITLE,    curses.COLOR_WHITE,   bg)
        curses.init_pair(CP_STAT,     curses.COLOR_GREEN,   bg)
        curses.init_pair(CP_MSG_GOOD, curses.COLOR_GREEN,   bg)
        curses.init_pair(CP_MSG_BAD,  curses.COLOR_RED,     bg)
        curses.init_pair(CP_MSG_INFO, curses.COLOR_CYAN,    bg)
        curses.init_pair(CP_DOOR,     curses.COLOR_YELLOW,  bg)
        curses.init_pair(CP_SELECT,   curses.COLOR_BLACK,   curses.COLOR_WHITE)
        curses.init_pair(CP_MON_G,    curses.COLOR_GREEN,   bg)
        curses.init_pair(CP_MON_Y,    curses.COLOR_YELLOW,  bg)
        curses.init_pair(CP_MON_W,    curses.COLOR_WHITE,   bg)
        curses.init_pair(CP_MON_C,    curses.COLOR_CYAN,    bg)
        curses.init_pair(CP_HP_HIGH,  curses.COLOR_GREEN,   bg)
        curses.init_pair(CP_HP_MED,   curses.COLOR_YELLOW,  bg)
        curses.init_pair(CP_HP_LOW,   curses.COLOR_RED,     bg)

    def _new_level(self):
        self.level = DungeonLevel(self.player.depth, self.player)
        self.player.x = self.level.entry_x
        self.player.y = self.level.entry_y
        self.msg(f"You descend to dungeon level {self.player.depth}...", CP_MSG_INFO)

    # ── Messages ──────────────────────────────────────────────

    def msg(self, text: str, cp: int = CP_DEFAULT):
        self.messages.append((text, cp))
        if len(self.messages) > 100:
            self.messages.pop(0)

    # ── Rendering ─────────────────────────────────────────────

    def _mon_color(self, col: str) -> int:
        return {"r": CP_MON_R, "g": CP_MON_G, "y": CP_MON_Y,
                "w": CP_MON_W, "c": CP_MON_C, "m": CP_STAIR}.get(col, CP_DEFAULT)

    def _safe_addch(self, y: int, x: int, ch, attr=0):
        try:
            self.scr.addch(y, x, ch, attr)
        except curses.error:
            pass

    def _safe_addstr(self, y: int, x: int, s: str, attr=0):
        try:
            self.scr.addstr(y, x, s, attr)
        except curses.error:
            pass

    def render(self):
        h, w = self.scr.getmaxyx()
        self.scr.erase()

        map_w  = w - self.PANEL_W - 1
        map_h  = h - self.MSG_H - 1
        lv     = self.level
        pl     = self.player

        # Camera centered on player
        cam_x = max(0, min(pl.x - map_w // 2, MAP_W - map_w))
        cam_y = max(0, min(pl.y - map_h // 2, MAP_H - map_h))

        # ── Draw map tiles ────────────────────────────────────
        for sy in range(map_h):
            wy = cam_y + sy
            if wy < 0 or wy >= MAP_H:
                continue
            for sx in range(map_w):
                wx = cam_x + sx
                if wx < 0 or wx >= MAP_W:
                    continue
                tile = lv.tiles[wy][wx]
                if tile == WALL:
                    self._safe_addch(sy, sx, '#',
                                     curses.color_pair(CP_WALL) | curses.A_DIM)
                elif tile == FLOOR:
                    self._safe_addch(sy, sx, '.',
                                     curses.color_pair(CP_FLOOR) | curses.A_DIM)
                elif tile == DOOR:
                    self._safe_addch(sy, sx, '+',
                                     curses.color_pair(CP_DOOR))
                elif tile == DOWN:
                    self._safe_addch(sy, sx, '>',
                                     curses.color_pair(CP_STAIR) | curses.A_BOLD)

        # ── Shopkeeper ────────────────────────────────────────
        if lv.shopkeeper:
            sk = lv.shopkeeper
            sx, sy = sk.x - cam_x, sk.y - cam_y
            if 0 <= sx < map_w and 0 <= sy < map_h:
                self._safe_addch(sy, sx, '$',
                                 curses.color_pair(CP_SHOP) | curses.A_BOLD)

        # ── Treasures ─────────────────────────────────────────
        for t in lv.treasures:
            sx, sy = t.x - cam_x, t.y - cam_y
            if 0 <= sx < map_w and 0 <= sy < map_h:
                ch = '*' if t.item else '$'
                self._safe_addch(sy, sx, ch,
                                 curses.color_pair(CP_TREASURE) | curses.A_BOLD)

        # ── Floor potions ─────────────────────────────────────
        for fx, fy in lv.floor_potions:
            sx, sy = fx - cam_x, fy - cam_y
            if 0 <= sx < map_w and 0 <= sy < map_h:
                self._safe_addch(sy, sx, '!',
                                 curses.color_pair(CP_MSG_GOOD) | curses.A_BOLD)

        # ── Floor allies (not yet picked up) ──────────────────
        for a in lv.floor_allies:
            sx, sy = a.x - cam_x, a.y - cam_y
            if 0 <= sx < map_w and 0 <= sy < map_h:
                self._safe_addch(sy, sx, a.ch,
                                 curses.color_pair(self._mon_color(a.col)) | curses.A_BOLD)

        # ── Monsters ──────────────────────────────────────────
        for m in lv.monsters:
            if not m.alive():
                continue
            sx, sy = m.x - cam_x, m.y - cam_y
            if 0 <= sx < map_w and 0 <= sy < map_h:
                self._safe_addch(sy, sx, m.ch,
                                 curses.color_pair(self._mon_color(m.col)) | curses.A_BOLD)

        # ── Active allies (following player) ──────────────────
        for a in pl.allies:
            if not a.alive():
                continue
            sx, sy = a.x - cam_x, a.y - cam_y
            if 0 <= sx < map_w and 0 <= sy < map_h:
                self._safe_addch(sy, sx, a.ch,
                                 curses.color_pair(self._mon_color(a.col)) | curses.A_BOLD)

        # ── Player ────────────────────────────────────────────
        px, py = pl.x - cam_x, pl.y - cam_y
        if 0 <= px < map_w and 0 <= py < map_h:
            self._safe_addch(py, px, '@',
                             curses.color_pair(CP_PLAYER) | curses.A_BOLD)

        # ── Vertical divider ──────────────────────────────────
        for y in range(h - self.MSG_H - 1):
            self._safe_addch(y, map_w, curses.ACS_VLINE,
                             curses.color_pair(CP_DEFAULT))

        # ── Stats panel ───────────────────────────────────────
        px0 = map_w + 1
        pw  = self.PANEL_W - 1

        def pline(row: int, text: str, cp: int = CP_DEFAULT, bold: bool = False):
            if 0 <= row < h:
                attr = curses.color_pair(cp)
                if bold:
                    attr |= curses.A_BOLD
                self._safe_addstr(row, px0, text[:pw], attr)

        pline(0,  " DJ's DUNGEON CRAWL", CP_TITLE, True)
        pline(1,  "-" * pw, CP_DEFAULT)
        pline(2,  f" Depth : {pl.depth}", CP_MSG_INFO)
        pline(3,  f" Level : {pl.level}", CP_STAT, True)
        pline(4,  f" Kills : {pl.kills}", CP_DEFAULT)
        pline(5,  "-" * pw, CP_DEFAULT)

        # HP bar
        hp_pct = pl.hp / pl.max_hp
        hp_cp  = CP_HP_HIGH if hp_pct > 0.6 else (CP_HP_MED if hp_pct > 0.3 else CP_HP_LOW)
        bar_l  = pw - 4
        filled = int(hp_pct * bar_l)
        bar    = "[" + "=" * filled + "-" * (bar_l - filled) + "]"
        pline(6,  " HP:", CP_DEFAULT)
        pline(7,  f" {bar}", hp_cp, True)
        pline(8,  f" {pl.hp} / {pl.max_hp}", hp_cp)

        # XP bar
        xp_pct = pl.xp / pl.xp_next
        xp_f   = int(xp_pct * bar_l)
        xp_bar = "[" + "=" * xp_f + "-" * (bar_l - xp_f) + "]"
        pline(9,  " XP:", CP_MSG_INFO)
        pline(10, f" {xp_bar}", CP_MSG_INFO)
        pline(11, f" {pl.xp} / {pl.xp_next}", CP_MSG_INFO)

        pline(12, "-" * pw, CP_DEFAULT)
        pline(13, f" Gold: {pl.gold} gp", CP_TREASURE, True)
        pline(14, "-" * pw, CP_DEFAULT)
        pline(15, " WEAPON:", CP_DEFAULT)
        pline(16, f"  {pl.weapon['name']}", CP_MON_Y)
        pline(17, f"  ATK: {pl.atk}", CP_MON_R)
        pline(18, " ARMOR:", CP_DEFAULT)
        pline(19, f"  {pl.armor['name']}", CP_MON_W)
        pline(20, f"  DEF: {pl.arm}", CP_STAT)
        pline(21, "-" * pw, CP_DEFAULT)
        if pl.potions:
            pline(22, f" Potions: {len(pl.potions)}", CP_MSG_GOOD)
        else:
            pline(22, " Potions: none", CP_WALL)

        # ── Active allies in panel ────────────────────────────
        panel_row = 23
        active_allies = [a for a in pl.allies if a.alive()]
        if active_allies:
            pline(panel_row, "-" * pw, CP_DEFAULT);  panel_row += 1
            pline(panel_row, " ALLIES", CP_MON_Y, True);  panel_row += 1
            for a in active_allies:
                if panel_row < h:
                    try:
                        self.scr.addch(panel_row, px0 + 1, a.ch,
                                       curses.color_pair(self._mon_color(a.col)) | curses.A_BOLD)
                        label = f" {a.name} ({a.moves_left})"
                        self.scr.addstr(panel_row, px0 + 2, label[:pw - 2],
                                        curses.color_pair(CP_DEFAULT))
                    except curses.error:
                        pass
                    panel_row += 1

        # ── Legend ────────────────────────────────────────────
        hint_row = h - self.MSG_H - 2
        legend_start = panel_row
        legend_end   = hint_row - 2   # leave room for separator + hint

        row = legend_start
        if row < legend_end:
            pline(row, "-" * pw, CP_DEFAULT);  row += 1
        if row < legend_end:
            pline(row, " LEGEND", CP_TITLE, True);  row += 1

        def draw_legend_entries(entries):
            nonlocal row
            for ch, cp, label in entries:
                if row >= legend_end:
                    break
                if 0 <= row < h:
                    try:
                        self.scr.addch(row, px0,     ' ')
                        self.scr.addch(row, px0 + 1, ch,
                                       curses.color_pair(cp) | curses.A_BOLD)
                        self.scr.addstr(row, px0 + 2, f"  {label}"[:pw - 2],
                                        curses.color_pair(CP_DEFAULT))
                    except curses.error:
                        pass
                row += 1

        if row < legend_end:
            pline(row, " MAP", CP_MSG_INFO);  row += 1
        draw_legend_entries(self.LEGEND_MAP)

        if row < legend_end:
            pline(row, " ALLIES", CP_MON_Y);  row += 1
        draw_legend_entries(self.LEGEND_ALLY)

        if row < legend_end:
            pline(row, " MONSTERS", CP_MSG_INFO);  row += 1
        draw_legend_entries(self.LEGEND_MON)

        # Controls hint at bottom of panel
        pline(hint_row - 1, "-" * pw, CP_DEFAULT)
        pline(hint_row,     " [i]nv [p]ot [?]help", CP_MSG_INFO)

        # ── Horizontal divider ────────────────────────────────
        div_row = h - self.MSG_H - 1
        if 0 <= div_row < h:
            try:
                self.scr.addch(div_row, 0, curses.ACS_LTEE,
                               curses.color_pair(CP_DEFAULT))
                for x in range(1, map_w):
                    self.scr.addch(div_row, x, curses.ACS_HLINE,
                                   curses.color_pair(CP_DEFAULT))
                self.scr.addch(div_row, map_w, curses.ACS_RTEE,
                               curses.color_pair(CP_DEFAULT))
            except curses.error:
                pass

        # ── Message log ───────────────────────────────────────
        recent = self.messages[-(self.MSG_H - 1):]
        for i, (text, cp) in enumerate(recent):
            row = h - self.MSG_H + i
            if 0 <= row < h:
                line = f"> {text}"
                self._safe_addstr(row, 0, line[:w - 1], curses.color_pair(cp))

        self.scr.refresh()

    # ── Movement & Actions ────────────────────────────────────

    def move(self, dx: int, dy: int):
        pl = self.player
        lv = self.level
        nx, ny = pl.x + dx, pl.y + dy

        # Bounds
        if not (0 <= nx < MAP_W and 0 <= ny < MAP_H):
            return

        # Attack monster
        m = lv.monster_at(nx, ny)
        if m:
            self._combat(m)
            return

        # Shopkeeper
        if lv.shopkeeper and lv.shopkeeper.x == nx and lv.shopkeeper.y == ny:
            self._shop()
            return

        # Wall check
        if not lv.walkable(nx, ny):
            return

        pl.x, pl.y = nx, ny

        # Pick up floor potion (instant full heal)
        if (nx, ny) in lv.floor_potions:
            lv.floor_potions.remove((nx, ny))
            pl.hp = pl.max_hp
            self.msg("You drink a Health Potion! HP fully restored!", CP_MSG_GOOD)

        # Pick up floor ally
        a = lv._ally_at(nx, ny)
        if a:
            lv.floor_allies.remove(a)
            pl.allies.append(a)
            self.msg(f"A {a.name} joins you for 50 moves!", CP_MON_Y)
            self._reposition_allies()

        # Pick up treasure
        t = lv.treasure_at(nx, ny)
        if t:
            lv.treasures.remove(t)
            pl.gold += t.gold
            parts = [f"You find {t.gold} gp!"]
            if t.item:
                parts.append(self._loot_item(t.item, t.itype))
            self.msg(" ".join(parts), CP_TREASURE)

        # Stairs notification
        if lv.tiles[ny][nx] == DOWN:
            self.msg("You stand on stairs leading down. Press ENTER to descend.", CP_STAIR)

        # Monsters take a turn
        self._monster_turns()

    def _reposition_allies(self):
        """Move each active ally to a free tile adjacent to the player."""
        pl  = self.player
        lv  = self.level
        dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]
        occupied = {(pl.x, pl.y)}
        for a in pl.allies:
            if not a.alive():
                continue
            candidates = [(pl.x + dx, pl.y + dy) for dx, dy in dirs]
            free = [pos for pos in candidates
                    if lv.walkable(*pos)
                    and not lv.monster_at(*pos)
                    and pos not in occupied]
            if free:
                free.sort(key=lambda p: abs(p[0] - a.x) + abs(p[1] - a.y))
                a.x, a.y = free[0]
            occupied.add((a.x, a.y))

    def _loot_item(self, item: dict, itype: str) -> str:
        pl = self.player
        if itype == "weapon":
            if item["atk"] > pl.weapon["atk"]:
                pl.weapon = item
                return f"Found {item['name']}! (equipped)"
            sell = max(1, item["cost"] // 5)
            pl.gold += sell
            return f"Found {item['name']}. (sold: {sell}gp)"
        elif itype == "armor":
            if item["arm"] > pl.armor["arm"]:
                pl.armor = item
                return f"Found {item['name']}! (equipped)"
            sell = max(1, item["cost"] // 5)
            pl.gold += sell
            return f"Found {item['name']}. (sold: {sell}gp)"
        elif itype == "potion":
            pl.potions.append(item)
            return f"Found a {item['name']}!"
        return ""

    def _use_stairs(self):
        lv = self.level
        if lv.tiles[self.player.y][self.player.x] == DOWN:
            self.player.depth += 1
            self._new_level()

    # ── Combat ────────────────────────────────────────────────

    def _combat(self, m: Monster):
        pl  = self.player
        dmg = pl.hit_monster(m)

        # Dwarf ally attacks the same target alongside the player
        dwarf_msg = ""
        for a in pl.allies:
            if a.alive() and a.atype == "dwarf":
                ddmg = m.take_hit(a.atk_roll(pl.level))
                dwarf_msg = f" Dwarf hits for {ddmg}!"
                break

        if not m.alive():
            gold    = m.loot_gold()
            pl.gold += gold
            leveled  = pl.gain_xp(m.xp)
            pl.kills += 1
            self.level.monsters.remove(m)
            self.msg(f"You slay the {m.name}! (+{m.xp} XP, +{gold} gp){dwarf_msg}", CP_MSG_GOOD)
            if leveled:
                self.msg(
                    f"*** LEVEL UP! You are now level {pl.level}! "
                    f"(HP+12, ATK+2, DEF+1) ***",
                    CP_TREASURE)
        else:
            mdmg = pl.take_hit(m)
            self.msg(
                f"You hit {m.name} for {dmg}.{dwarf_msg} "
                f"It strikes back for {mdmg}! "
                f"({m.name} HP:{m.hp}/{m.max_hp})",
                CP_DEFAULT)
            if not pl.alive():
                self._game_over()
                return

        self._monster_turns()

    def _monster_turns(self):
        pl = self.player
        lv = self.level

        # ── Elf: ranged attack on nearest monster within 5 tiles ──
        for a in pl.allies:
            if not a.alive() or a.atype != "elf":
                continue
            targets = [m for m in lv.monsters if m.alive() and
                       abs(m.x - pl.x) + abs(m.y - pl.y) <= 5]
            if targets:
                target = min(targets, key=lambda m: abs(m.x-pl.x)+abs(m.y-pl.y))
                edgm = target.take_hit(a.atk_roll(pl.level))
                if not target.alive():
                    gold = target.loot_gold()
                    pl.gold += gold
                    pl.gain_xp(target.xp)
                    pl.kills += 1
                    lv.monsters.remove(target)
                    self.msg(f"Elf shoots the {target.name}! Slain! (+{gold} gp)", CP_MON_G)
                else:
                    self.msg(f"Elf shoots {target.name} for {edgm} dmg "
                             f"(HP:{target.hp}/{target.max_hp})", CP_MON_G)
            break  # only one elf

        # ── Ally countdown & cleanup ───────────────────────────
        for a in list(pl.allies):
            a.moves_left -= 1
            if not a.alive():
                pl.allies.remove(a)
                self.msg(f"Your {a.name} has departed after 50 moves.", CP_MSG_INFO)

        # ── Reposition allies ──────────────────────────────────
        self._reposition_allies()

        for m in list(lv.monsters):
            if not m.alive():
                continue
            dist = abs(m.x - pl.x) + abs(m.y - pl.y)
            if dist <= 1:
                mdmg = pl.take_hit(m)
                self.msg(f"The {m.name} attacks you for {mdmg} damage!", CP_MSG_BAD)
                if not pl.alive():
                    self._game_over()
                    return
            elif dist < 18:
                # Chase player
                dx = 0 if m.x == pl.x else (1 if m.x < pl.x else -1)
                dy = 0 if m.y == pl.y else (1 if m.y < pl.y else -1)
                for ddx, ddy in [(dx, dy), (dx, 0), (0, dy)]:
                    if ddx == 0 and ddy == 0:
                        continue
                    nx, ny = m.x + ddx, m.y + ddy
                    if (lv.walkable(nx, ny) and
                            not lv.monster_at(nx, ny) and
                            (nx, ny) != (pl.x, pl.y)):
                        m.x, m.y = nx, ny
                        break

    # ── Shop ──────────────────────────────────────────────────

    def _shop(self):
        sk = self.level.shopkeeper
        if not sk:
            return
        selected = 0

        while True:
            self.render()
            h, w = self.scr.getmaxyx()
            bh = min(len(sk.stock) + 8, h - 4)
            bw = min(52, w - 4)
            by = (h - bh) // 2
            bx = (w - bw) // 2

            # Background fill
            for y in range(by, by + bh):
                self._safe_addstr(y, bx, " " * bw, curses.color_pair(CP_DEFAULT))

            # Border
            try:
                self.scr.addstr(by,         bx, "+" + "-" * (bw - 2) + "+",
                                curses.color_pair(CP_SHOP) | curses.A_BOLD)
                self.scr.addstr(by + bh - 1, bx, "+" + "-" * (bw - 2) + "+",
                                curses.color_pair(CP_SHOP) | curses.A_BOLD)
                for y in range(by + 1, by + bh - 1):
                    self.scr.addch(y, bx,        '|', curses.color_pair(CP_SHOP) | curses.A_BOLD)
                    self.scr.addch(y, bx + bw - 1,'|', curses.color_pair(CP_SHOP) | curses.A_BOLD)
            except curses.error:
                pass

            title = "THE MERCHANT'S WARES"
            self._safe_addstr(by + 1, bx + (bw - len(title)) // 2, title,
                              curses.color_pair(CP_SHOP) | curses.A_BOLD)
            self._safe_addstr(by + 2, bx + 2,
                              f"Your gold: {self.player.gold} gp",
                              curses.color_pair(CP_TREASURE) | curses.A_BOLD)
            self._safe_addstr(by + 3, bx + 1, "-" * (bw - 2),
                              curses.color_pair(CP_SHOP))

            for i, item in enumerate(sk.stock):
                row = by + 4 + i
                if row >= by + bh - 3:
                    break
                can_buy = self.player.gold >= item["cost"]
                if i == selected:
                    attr = curses.color_pair(CP_SELECT) | curses.A_BOLD
                elif not can_buy:
                    attr = curses.color_pair(CP_WALL) | curses.A_DIM
                else:
                    attr = curses.color_pair(CP_DEFAULT)

                itype = item.get("itype", "")
                if itype == "weapon":
                    stat = f"ATK+{item['atk']}"
                elif itype == "armor":
                    stat = f"DEF+{item['arm']}"
                else:
                    stat = "Full HP"
                line = f"  {item['name']:<22} {stat:<10} {item['cost']} gp"
                self._safe_addstr(row, bx + 1, line[:bw - 2], attr)

            footer = by + bh - 2
            self._safe_addstr(footer, bx + 2,
                              "UP/DOWN=select  ENTER=buy  ESC=leave",
                              curses.color_pair(CP_MSG_INFO))
            self.scr.refresh()

            key = self.scr.getch()
            if key == curses.KEY_UP:
                selected = max(0, selected - 1)
            elif key == curses.KEY_DOWN:
                selected = min(len(sk.stock) - 1, selected + 1)
            elif key in (curses.KEY_ENTER, 10, 13):
                item = sk.stock[selected]
                if self.player.gold >= item["cost"]:
                    self.player.gold -= item["cost"]
                    itype = item.get("itype", "")
                    if itype == "weapon":
                        self.player.weapon = {k: v for k, v in item.items() if k != "itype"}
                        self.msg(f"You buy the {item['name']}! (equipped)", CP_MSG_GOOD)
                    elif itype == "armor":
                        self.player.armor = {k: v for k, v in item.items() if k != "itype"}
                        self.msg(f"You buy the {item['name']}! (equipped)", CP_MSG_GOOD)
                    elif itype == "potion":
                        self.player.potions.append(
                            {k: v for k, v in item.items() if k != "itype"})
                        self.msg(f"You buy a {item['name']}!", CP_MSG_GOOD)
                else:
                    self.msg("Not enough gold!", CP_MSG_BAD)
            elif key in (27, ord('q'), ord(' ')):
                break

    # ── Help & Inventory overlays ─────────────────────────────

    def _help(self):
        h, w = self.scr.getmaxyx()
        lines = [
            "+------------------------------+",
            "|     DUNGEON CRAWL  HELP      |",
            "+------------------------------+",
            "| Arrow keys   Move / Attack   |",
            "| ENTER        Use stairs (>)  |",
            "| p            Drink potion    |",
            "| i            Inventory       |",
            "| ?            This help       |",
            "| q / ESC      Quit            |",
            "+------------------------------+",
            "|  @  You                      |",
            "|  .  Floor      #  Wall       |",
            "|  >  Stairs     +  Door       |",
            "|  $  Treasure / Shop          |",
            "|  *  Item on ground           |",
            "+------------------------------+",
            "  Press any key to continue    ",
        ]
        sy = max(0, (h - len(lines)) // 2)
        sx = max(0, (w - 34) // 2)
        for i, line in enumerate(lines):
            self._safe_addstr(sy + i, sx, line,
                              curses.color_pair(CP_SHOP) | curses.A_BOLD)
        self.scr.refresh()
        self.scr.getch()

    def _inventory(self):
        pl = self.player
        h, w = self.scr.getmaxyx()
        lines = [
            "+------------------------------------+",
            "|            INVENTORY               |",
            "+------------------------------------+",
            f"| Weapon : {pl.weapon['name']:<26} |",
            f"|   ATK  : {pl.atk:<26} |",
            f"| Armor  : {pl.armor['name']:<26} |",
            f"|   DEF  : {pl.arm:<26} |",
            "+------------------------------------+",
            f"| Gold   : {pl.gold} gp{'':<21} |",
            f"| Level  : {pl.level:<26} |",
            f"| XP     : {pl.xp}/{pl.xp_next:<22} |",
            f"| HP     : {pl.hp}/{pl.max_hp:<23} |",
            f"| Kills  : {pl.kills:<26} |",
            f"| Depth  : {pl.depth:<26} |",
            "+------------------------------------+",
        ]
        if pl.potions:
            lines.append(f"| Potions: {len(pl.potions):<26} |")
            for i, pot in enumerate(pl.potions[:5]):
                lines.append(f"|   {i+1}. {pot['name']:<30} |")
        else:
            lines.append("|  No potions in pack.               |")
        lines.append("+------------------------------------+")
        lines.append("   Press any key to close            ")

        sy = max(0, (h - len(lines)) // 2)
        sx = max(0, (w - 40) // 2)
        for i, line in enumerate(lines):
            self._safe_addstr(sy + i, sx, line[:w - sx - 1],
                              curses.color_pair(CP_MSG_INFO) | curses.A_BOLD)
        self.scr.refresh()
        self.scr.getch()

    # ── Game over / Death ─────────────────────────────────────

    def _game_over(self):
        self.running = False
        pl = self.player
        self.render()
        h, w = self.scr.getmaxyx()
        lines = [
            "+====================================+",
            "|          *** YOU DIED ***          |",
            "+====================================+",
            f"|  Dungeon Depth : {pl.depth:<18} |",
            f"|  Character Lvl : {pl.level:<18} |",
            f"|  Monsters Slain: {pl.kills:<18} |",
            f"|  Gold Collected: {pl.gold} gp{'':<13} |",
            "+====================================+",
            "|                                    |",
            "|      Press any key to exit         |",
            "+====================================+",
        ]
        sy = max(0, (h - len(lines)) // 2)
        sx = max(0, (w - 40) // 2)
        for i, line in enumerate(lines):
            self._safe_addstr(sy + i, sx, line,
                              curses.color_pair(CP_MSG_BAD) | curses.A_BOLD)
        self.scr.refresh()
        self.scr.getch()

    # ── Title screen ──────────────────────────────────────────

    def _title(self):
        self.scr.erase()
        h, w = self.scr.getmaxyx()

        # Big ASCII-art letters for "DJ's"
        djs = [
            r"  ____        _    _____ ",
            r" |  _ \      | |  / ____|",
            r" | | | |     | | | (___  ",
            r" | | | |  _  | |  \___ \ ",
            r" | |/ /  | |_| |  ____) |",
            r" |___/    \___/  |_____/ ",
        ]
        # Box frame around the full title
        BW = 56
        box = [
            "+" + "=" * BW + "+",
            "|" + " " * BW + "|",
        ]
        for line in djs:
            padded = line.center(BW)
            box.append("|" + padded + "|")
        box += [
            "|" + " " * BW + "|",
            "|" + "DUNGEON  CRAWL".center(BW) + "|",
            "|" + " " * BW + "|",
            "|" + "~ A D&D Style Terminal Adventure ~".center(BW) + "|",
            "|" + " " * BW + "|",
            "+" + "=" * BW + "+",
        ]

        controls = [
            "",
            "  Arrow Keys ......... Move / Attack",
            "  ENTER .............. Descend Stairs (>)",
            "  p .................. Drink Potion",
            "  i .................. Inventory",
            "  ? .................. Help",
            "  q / ESC ............ Quit",
            "",
            "  Battle monsters. Find treasure. Visit the merchant.",
            "  How deep into the dungeon can you survive?",
            "",
            "           >>> Press any key to begin your quest <<<",
        ]

        total = len(box) + len(controls) + 1
        start_y = max(1, (h - total) // 2)

        for i, line in enumerate(box):
            x = max(0, (w - len(line)) // 2)
            # Title line gets special color
            if "DUNGEON  CRAWL" in line:
                attr = curses.color_pair(CP_MON_Y) | curses.A_BOLD
            elif "DJ" in line or any(c in line for c in ["_", "|", "("]):
                attr = curses.color_pair(CP_TREASURE) | curses.A_BOLD
            elif line.startswith("+"):
                attr = curses.color_pair(CP_SHOP) | curses.A_BOLD
            elif "Style" in line:
                attr = curses.color_pair(CP_MSG_INFO)
            else:
                attr = curses.color_pair(CP_SHOP) | curses.A_BOLD
            self._safe_addstr(start_y + i, x, line, attr)

        cy = start_y + len(box) + 1
        for i, line in enumerate(controls):
            cp = CP_TREASURE if ">>>" in line else CP_DEFAULT
            self._safe_addstr(cy + i, max(0, (w - 56) // 2), line,
                              curses.color_pair(cp) | (curses.A_BOLD if ">>>" in line else 0))

        self.scr.refresh()
        self.scr.getch()

    # ── Main loop ─────────────────────────────────────────────

    def run(self):
        curses.curs_set(0)
        self.scr.keypad(True)
        self._title()
        self.render()
        while self.running:
            key = self.scr.getch()
            if key == -1:
                continue
            if key in (ord('q'), 27):
                self.running = False
            elif key == curses.KEY_UP:
                self.move(0, -1)
            elif key == curses.KEY_DOWN:
                self.move(0, 1)
            elif key == curses.KEY_LEFT:
                self.move(-1, 0)
            elif key == curses.KEY_RIGHT:
                self.move(1, 0)
            elif key in (curses.KEY_ENTER, 10, 13):
                self._use_stairs()
            elif key == ord('p'):
                result = self.player.drink_potion()
                if result:
                    self.msg(result, CP_MSG_GOOD)
                else:
                    self.msg("You have no potions!", CP_MSG_BAD)
            elif key == ord('i'):
                self._inventory()
            elif key == ord('?'):
                self._help()
            if self.running:
                self.render()


# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

def main(stdscr):
    game = Game(stdscr)
    game.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        raise
