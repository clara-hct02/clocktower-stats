import os, json, sqlite3

path_to_json_files = 'data/games/';

conn = sqlite3.connect('botc.db')
conn.execute("PRAGMA foreign_keys = ON")

with open("schema.sql", encoding="utf-8") as f:
    conn.executescript(f.read())

with open("data/roles.json", encoding="utf-8") as file:
    data = json.load(file)

    for role in data:
        conn.execute("""
            INSERT INTO roles (name, team) VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET
                team = excluded.team
        """, (role["name"], role["team"]))

for root, dirs, files in os.walk(path_to_json_files):
    for n in files:
        with open(os.path.join(root, n)) as json_file:
            game = json.load(json_file)

            conn.execute("""
                INSERT INTO games (id, script, date, storyteller, group_name, winner, player_count, traveller_count, loric)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE set
                    script = excluded.script,
                    date = excluded.date,
                    storyteller = excluded.storyteller,
                    group_name = excluded.group_name,
                    winner = excluded.winner,
                    player_count = excluded.player_count,
                    traveller_count = excluded.traveller_count,
                    loric = excluded.loric
                """,  (game["id"], game["script"], game["date"], game["storyteller"], game["group_name"], 
                        game["winner"],
                        game["player_count"],
                        game.get("traveller_count", 0),
                        game.get("loric", False)))


            for p in game["players"]:
                conn.execute("""
                    INSERT OR IGNORE INTO players (game_id, name, role, secondary_role, team)
                    VALUES (?, ?, ?, ?, ?)
                """, 
                (game["id"], p["name"], p["role"], p.get("secondary_role"), p["team"]))


winRates = conn.execute("""
    SELECT gp.name,
        COUNT(*) AS games,
        SUM(gp.team = g.winner) AS wins,
        ROUND(AVG(gp.team = g.winner), 3) AS win_rate
    FROM players gp
    JOIN games g ON g.id = gp.game_id
    GROUP BY gp.name
    ORDER BY games DESC
""").fetchall()

print(winRates)

goodWins = conn.execute("""
    SELECT games.group_name,
        ROUND(AVG("good" = games.winner), 3) AS win_rate
    FROM games
    GROUP BY games.group_name
""").fetchall()

print(goodWins)

conn.commit()
conn.close()

