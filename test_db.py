from app.database import get_connection

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM batteries")

        for row in cur.fetchall():
            print(row)