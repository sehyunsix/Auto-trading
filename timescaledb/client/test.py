import psycopg2

##example get open price
CONNECTION = "postgres://sehyun:1234@ec2-3-25-126-189.ap-southeast-2.compute.amazonaws.com:5432/root"
with psycopg2.connect(CONNECTION) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT open_time, open_price FROM ethusdt WHERE open_time > '2021-01-01 00:00:00' AND open_time < '2021-01-02 00:00:00'"
        )
        print(cur.fetchall())
