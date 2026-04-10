import os
import time
import pymysql


def parse_database_url(url: str):
    if not url.startswith("mysql+pymysql://"):
        raise ValueError("DATABASE_URL must start with mysql+pymysql://")

    payload = url.replace("mysql+pymysql://", "", 1)
    credentials, remainder = payload.split("@", 1)
    user, password = credentials.split(":", 1)
    host_port, database = remainder.split("/", 1)

    if ":" in host_port:
        host, port = host_port.rsplit(":", 1)
        port = int(port)
    else:
        host, port = host_port, 3306

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
    }


def wait_for_db():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set.")

    connection_settings = parse_database_url(database_url)
    max_attempts = int(os.getenv("DB_MAX_ATTEMPTS", "30"))
    sleep_seconds = int(os.getenv("DB_WAIT_SECONDS", "2"))

    for attempt in range(1, max_attempts + 1):
        try:
            connection = pymysql.connect(**connection_settings)
            connection.close()
            print("Database connection established.")
            return
        except Exception as exc:
            print(f"Database not ready yet (attempt {attempt}/{max_attempts}): {exc}")
            time.sleep(sleep_seconds)

    raise RuntimeError("Could not connect to the database in time.")


if __name__ == "__main__":
    wait_for_db()
