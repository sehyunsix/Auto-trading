import psycopg2
from env import DATA_BASE_URL

##example get open price
CONNECTION = DATA_BASE_URL
with psycopg2.connect(CONNECTION) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT open_time, open_price FROM ethusdt WHERE open_time > '2021-01-01 00:00:00' AND open_time < '2021-01-02 00:00:00'"
        )
        print(cur.fetchall())
