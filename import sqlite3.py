import sqlite3

class Database:
    def __init__(self, db_name="app.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        # Players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT UNIQUE NOT NULL,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        # Races table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS races (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
        ''')
        # Character Classes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character_classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
        ''')
        # Characters table (update to reference race and class)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                name TEXT NOT NULL,
                race_id INTEGER,
                class_id INTEGER,
                level INTEGER DEFAULT 1,
                hp INTEGER DEFAULT 100,
                mp INTEGER DEFAULT 50,
                FOREIGN KEY(player_id) REFERENCES players(id),
                FOREIGN KEY(race_id) REFERENCES races(id),
                FOREIGN KEY(class_id) REFERENCES character_classes(id)
            )
        ''')
        # Items table (expanded for Diablo-style, with prefixes/suffixes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL, -- e.g., weapon, armor, potion, crafting
                subtype TEXT,       -- e.g., sword, shield, helmet, rune
                rarity TEXT NOT NULL, -- e.g., common, magic, rare, legendary, set, unique
                level_required INTEGER DEFAULT 1,
                damage_min INTEGER,
                damage_max INTEGER,
                defense INTEGER,
                attributes TEXT,    -- JSON or comma-separated (e.g., "+10 STR, +5% Fire Resist")
                sockets INTEGER DEFAULT 0,
                prefix1 TEXT,
                prefix1_tier INTEGER,
                prefix2 TEXT,
                prefix2_tier INTEGER,
                suffix1 TEXT,
                suffix1_tier INTEGER,
                suffix2 TEXT,
                suffix2_tier INTEGER,
                description TEXT
            )
        ''')
        # Crafting recipes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crafting_recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                result_item_id INTEGER,
                ingredients TEXT, -- JSON or comma-separated item IDs and quantities
                description TEXT,
                FOREIGN KEY(result_item_id) REFERENCES items(id)
            )
        ''')
        # Monsters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monsters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL, -- e.g., demon, undead, beast, boss
                level INTEGER DEFAULT 1,
                hp INTEGER DEFAULT 100,
                damage_min INTEGER,
                damage_max INTEGER,
                abilities TEXT, -- JSON or comma-separated
                loot_table TEXT -- JSON or comma-separated item IDs
            )
        ''')
        # Quests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                reward TEXT
            )
        ''')
        # Skills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT, -- e.g., Barbarian, Sorcerer
                description TEXT,
                mana_cost INTEGER DEFAULT 0,
                cooldown REAL DEFAULT 0,
                damage INTEGER,
                effect TEXT -- e.g., "Stun", "Freeze", etc.
            )
        ''')

        # Spells table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spells (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT, -- e.g., Sorcerer, Necromancer
                description TEXT,
                mana_cost INTEGER DEFAULT 0,
                cooldown REAL DEFAULT 0,
                damage INTEGER,
                effect TEXT -- e.g., "Burn", "Poison", etc.
            )
        ''')

        self.conn.commit()

    def get_connection(self):
        return self.conn

    def insert_diablo4_sample_data(self):
        cursor = self.conn.cursor()
        # Sample Items (Weapons & Armors)
        cursor.execute("""
            INSERT INTO items (name, type, subtype, rarity, level_required, damage_min, damage_max, defense, attributes, sockets, description)
            VALUES
            ('Doombringer', 'weapon', 'sword', 'unique', 80, 1200, 1500, NULL, '+20% Crit, +10% Life Steal', 3, 'A legendary sword that brings doom to its foes.'),
            ('Harlequin Crest', 'armor', 'helm', 'unique', 75, NULL, NULL, 500, '+10 All Stats, +20% Damage Reduction', 2, 'A mythical helm known as Shako.'),
            ('Tempest Roar', 'armor', 'helm', 'unique', 80, NULL, NULL, 520, '+30% Lightning Resist, +2 to All Skills', 1, 'A helm that crackles with storm energy.')
        """)
        # Sample Crafting Recipe
        cursor.execute("""
            INSERT INTO crafting_recipes (name, result_item_id, ingredients, description)
            VALUES
            ('Socketed Sword Recipe', 1, 'Iron Ore:10,Gold:5000', 'Craft a socketed sword using iron ore and gold.')
        """)
        # Sample Monster
        cursor.execute("""
            INSERT INTO monsters (name, type, level, hp, damage_min, damage_max, abilities, loot_table)
            VALUES
            ('Lilith', 'boss', 100, 50000, 800, 1200, 'Blood Nova,Charm,Teleport', '1,2,3'),
            ('Fallen', 'demon', 10, 150, 10, 20, 'Fireball', '1')
        """)
        # Sample Skills
        cursor.execute("""
            INSERT INTO skills (name, class, description, mana_cost, cooldown, damage, effect)
            VALUES
            ('Whirlwind', 'Barbarian', 'Spin and deal damage to all nearby enemies.', 25, 0.5, 350, 'AOE Damage'),
            ('Blood Surge', 'Necromancer', 'Draw blood from enemies and explode it.', 30, 1.0, 400, 'Life Steal'),
            ('Chain Lightning', 'Sorcerer', 'Unleash lightning that jumps between enemies.', 20, 0.8, 320, 'Chain, Shock')
        """)
        # Sample Spells
        cursor.execute("""
            INSERT INTO spells (name, class, description, mana_cost, cooldown, damage, effect)
            VALUES
            ('Fireball', 'Sorcerer', 'Hurl a fiery ball that explodes on impact.', 20, 1.2, 300, 'Burn'),
            ('Bone Spear', 'Necromancer', 'Summon a spear of bone that pierces enemies.', 25, 1.0, 350, 'Pierce'),
            ('Pulverize', 'Druid', 'Smash the ground to deal damage in an area.', 30, 1.5, 400, 'Stun')
        """)
        self.conn.commit()

    def insert_dnd5e_sample_data(self):
        cursor = self.conn.cursor()
        # D&D 5e Weapons
        cursor.execute("""
            INSERT INTO items (name, type, subtype, rarity, level_required, damage_min, damage_max, defense, attributes, sockets, description)
            VALUES
            ('Longsword', 'weapon', 'sword', 'common', 1, 1, 8, NULL, '+0 ATK', 0, 'Versatile (1d8 slashing)'),
            ('Great Axe', 'weapon', 'axe', 'uncommon', 3, 1, 12, NULL, '+0 ATK', 0, 'Heavy, two-handed (1d12 slashing)'),
            ('Shortbow', 'weapon', 'bow', 'common', 1, 1, 6, NULL, '+0 ATK', 0, 'Range (80/320), two-handed (1d6 piercing)')
        """)
        # D&D 5e Armor
        cursor.execute("""
            INSERT INTO items (name, type, subtype, rarity, level_required, damage_min, damage_max, defense, attributes, sockets, description)
            VALUES
            ('Chain Mail', 'armor', 'heavy', 'common', 1, NULL, NULL, 16, 'Disadvantage on Stealth', 0, 'Heavy armor (AC 16)'),
            ('Leather Armor', 'armor', 'light', 'common', 1, NULL, NULL, 11, 'No Stealth Penalty', 0, 'Light armor (AC 11 + DEX)'),
            ('Shield', 'armor', 'shield', 'common', 1, NULL, NULL, 2, '+2 AC', 0, 'Shield (AC +2)')
        """)
        # D&D 5e Rings & Necklaces
        cursor.execute("""
            INSERT INTO items (name, type, subtype, rarity, level_required, damage_min, damage_max, defense, attributes, sockets, description)
            VALUES
            ('Ring of Protection', 'accessory', 'ring', 'rare', 5, NULL, NULL, 1, '+1 AC, +1 Saving Throws', 0, 'A magical ring that grants protection.'),
            ('Amulet of Health', 'accessory', 'neck', 'rare', 8, NULL, NULL, NULL, 'Sets CON to 19', 0, 'A magical amulet that increases Constitution.')
        """)
        # D&D 5e Other Equipment
        cursor.execute("""
            INSERT INTO items (name, type, subtype, rarity, level_required, damage_min, damage_max, defense, attributes, sockets, description)
            VALUES
            ('Cloak of Invisibility', 'accessory', 'cloak', 'legendary', 15, NULL, NULL, NULL, 'Invisibility (1 hour/day)', 0, 'A cloak that grants invisibility.'),
            ('Boots of Speed', 'accessory', 'boots', 'rare', 10, NULL, NULL, NULL, 'Double movement speed', 0, 'Boots that double your speed.')
        """)
        # D&D 5e Monsters
        cursor.execute("""
            INSERT INTO monsters (name, type, level, hp, damage_min, damage_max, abilities, loot_table)
            VALUES
            ('Goblin', 'humanoid', 1, 7, 1, 6, 'Nimble Escape', '4,5'),
            ('Orc', 'humanoid', 2, 15, 1, 12, 'Aggressive', '1,6'),
            ('Adult Red Dragon', 'dragon', 17, 256, 2, 24, 'Fire Breath, Legendary Resistance', '3,7,8')
        """)
        # D&D 5e Gear Ruleset (as a quest or info entry)
        cursor.execute("""
            INSERT INTO quests (title, description, reward)
            VALUES
            ('D&D 5e Gear Rules', 'You can equip: 1 armor, 1 shield, 2 rings, 1 amulet/necklace, 1 cloak, 1 pair of boots, 1 main weapon, 1 offhand weapon or shield.', 'Knowledge')
        """)
        self.conn.commit()