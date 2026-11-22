CREATE TABLE IF NOT EXISTS roles (
  name        TEXT PRIMARY KEY,
  team        TEXT
);

CREATE TABLE IF NOT EXISTS games (
  id                TEXT PRIMARY KEY,
  script            TEXT,
  date              TEXT,
  storyteller       TEXT,
  group_name        TEXT,
  winner            TEXT,
  player_count      INTEGER,
  traveller_count   INTEGER,
  loric             BOOLEAN
);

CREATE TABLE IF NOT EXISTS players (
  name              TEXT,
  game_id           INTEGER REFERENCES games(id),
  role              TEXT REFERENCES roles(name),
  secondary_role    TEXT REFERENCES roles(name),
  team              TEXT,
  PRIMARY KEY (game_id, name)
);