-- JUMPCHAIN ENGINE DATABASE SCHEMA
-- SQLite schema for persistent jumpchain game state

-- Core jumper character
CREATE TABLE IF NOT EXISTS jumper (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER DEFAULT 18,
    current_jump TEXT,
    total_cp_earned INTEGER DEFAULT 1000,
    total_cp_spent INTEGER DEFAULT 0,
    jump_count INTEGER DEFAULT 0,
    current_year INTEGER DEFAULT 1,
    current_day INTEGER DEFAULT 1,
    current_location TEXT DEFAULT 'Starting Area',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Perks and powers
CREATE TABLE IF NOT EXISTS perks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    owner_type TEXT NOT NULL CHECK(owner_type IN ('jumper', 'companion')),
    name TEXT NOT NULL,
    source_jump TEXT NOT NULL,
    cp_cost INTEGER DEFAULT 0,
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    evolution_stage INTEGER DEFAULT 0,
    synergy_tags TEXT, -- JSON array of tags for synergy detection
    mechanics TEXT,    -- JSON object with mechanical effects
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES jumper(id) ON DELETE CASCADE
);

-- Companions
CREATE TABLE IF NOT EXISTS companions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    origin TEXT,
    source_jump TEXT NOT NULL,
    cp_budget INTEGER DEFAULT 600,
    cp_spent INTEGER DEFAULT 0,
    relationship_level INTEGER DEFAULT 5 CHECK(relationship_level BETWEEN 1 AND 10),
    is_active BOOLEAN DEFAULT 1,
    personality_profile TEXT, -- JSON with personality traits
    current_activity TEXT,
    traits TEXT,  -- JSON with trait scores
    goals TEXT,   -- JSON array of goals
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items and equipment
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    owner_type TEXT NOT NULL CHECK(owner_type IN ('jumper', 'companion')),
    name TEXT NOT NULL,
    source_jump TEXT NOT NULL,
    cp_cost INTEGER DEFAULT 0,
    description TEXT,
    quantity INTEGER DEFAULT 1,
    is_equipped BOOLEAN DEFAULT 0,
    properties TEXT, -- JSON with item mechanics
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jump history
CREATE TABLE IF NOT EXISTS jump_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jump_name TEXT NOT NULL,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    duration_years INTEGER DEFAULT 10,
    scenario_completed BOOLEAN DEFAULT 0,
    rewards_earned TEXT, -- JSON with rewards
    major_events TEXT,   -- JSON array of key moments
    success_rating INTEGER CHECK(success_rating BETWEEN 1 AND 10),
    notes TEXT
);

-- World state for current jump
CREATE TABLE IF NOT EXISTS world_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jump_name TEXT NOT NULL UNIQUE,
    current_date TEXT,
    current_year INTEGER DEFAULT 1,
    current_day INTEGER DEFAULT 1,
    key_events TEXT,          -- JSON array of timeline events
    factions TEXT,            -- JSON object with faction states
    known_characters TEXT,    -- JSON object with NPC states
    active_threats TEXT,      -- JSON array of current threats
    completed_objectives TEXT, -- JSON array
    available_objectives TEXT, -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Active drawbacks (temporary per jump)
CREATE TABLE IF NOT EXISTS active_drawbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jump_name TEXT NOT NULL,
    name TEXT NOT NULL,
    cp_value INTEGER NOT NULL,
    description TEXT,
    expires_with_jump BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progression rewards and achievements
CREATE TABLE IF NOT EXISTS rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('bronze', 'silver', 'gold', 'platinum')),
    trigger_condition TEXT,
    reward_value REAL,  -- CP multiplier or bonus
    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    icon TEXT
);

-- Background events (adversary actions, off-screen)
CREATE TABLE IF NOT EXISTS background_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    turn_number INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    faction TEXT,
    description TEXT NOT NULL,
    impact_level INTEGER CHECK(impact_level BETWEEN 1 AND 10),
    player_aware BOOLEAN DEFAULT 0,
    resolution_deadline TEXT,
    consequences TEXT, -- JSON with potential outcomes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Turn log (for replay/analysis)
CREATE TABLE IF NOT EXISTS turn_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    turn_number INTEGER NOT NULL,
    jump_name TEXT NOT NULL,
    player_action TEXT NOT NULL,
    mechanical_result TEXT,  -- JSON
    narration TEXT,
    achievements_earned TEXT, -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_perks_owner ON perks(owner_id, owner_type);
CREATE INDEX IF NOT EXISTS idx_perks_active ON perks(is_active);
CREATE INDEX IF NOT EXISTS idx_items_owner ON items(owner_id, owner_type);
CREATE INDEX IF NOT EXISTS idx_companions_active ON companions(is_active);
CREATE INDEX IF NOT EXISTS idx_background_events_turn ON background_events(turn_number);
CREATE INDEX IF NOT EXISTS idx_turn_log_jump ON turn_log(jump_name);

-- Initial data (create default jumper)
INSERT OR IGNORE INTO jumper (id, name, age, current_jump)
VALUES (1, 'Jumper', 18, 'None');
