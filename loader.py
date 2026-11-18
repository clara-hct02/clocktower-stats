import os, json, sqlite3

path_to_json_files = 'data/games/';

conn = sqlite3.connect('botc.db')

with open("data/roles.json", encoding="utf-8") as file:
    data = json.load(file)

conn.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        name TEXT PRIMARY KEY,
        team TEXT
    )
""")

for role in data:
    conn.execute("""
    INSERT INTO roles (name, team) VALUES (?, ?)
    ON CONFLICT(name) DO UPDATE SET team = excluded.team
    """,(role["name"], role["team"]))

conn.commit()
conn.close()

