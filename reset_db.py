import psycopg2

try:
    conn = psycopg2.connect(
        dbname="Property",
        user="postgres",
        password="admin",
        host="127.0.0.1",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()
    print("Connected to PostgreSQL. Dropping public schema to reset database...")
    cur.execute("DROP SCHEMA public CASCADE;")
    cur.execute("CREATE SCHEMA public;")
    cur.execute("GRANT ALL ON SCHEMA public TO postgres;")
    cur.execute("GRANT ALL ON SCHEMA public TO public;")
    print("Database reset successfully.")
    cur.close()
    conn.close()
except Exception as e:
    print("An error occurred:", e)
