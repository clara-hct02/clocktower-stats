roles (
  name        TEXT PRIMARY KEY,
  team        TEXT,
);

games (
  id          INTEGER PRIMARY KEY,
  script      TEXT,
  date        TEXT,
  storyteller TEXT
  winner      TEXT
);

players (
  game_id     INTEGER REFERENCES games(id),
  name        TEXT,
  role        TEXT REFERENCES roles(name),
  team        TEXT,
  PRIMARY KEY (game_id, name)
);