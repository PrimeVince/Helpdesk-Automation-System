import sqlite3
from pathlib import Path
from contextlib import contextmanager

DATABASE_PATH = Path(__file__).parent.parent / "data" / "helpdesk.db"


@contextmanager
def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def initialize_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL CHECK (length(trim(user_name)) > 0),
                department TEXT NOT NULL CHECK (length(trim(department)) > 0),
                issue TEXT NOT NULL CHECK (length(trim(issue)) > 0),

                category TEXT NOT NULL CHECK (
                    category IN (
                        'Hardware',
                        'Software',
                        'Network',
                        'Account & Access',
                        'Other'
                    )
                ),

                priority TEXT NOT NULL CHECK (
                    priority IN ('Low', 'Medium', 'High', 'Critical')
                ),

                status TEXT NOT NULL DEFAULT 'Open' CHECK (
                    status IN ('Open', 'In Progress', 'Resolved', 'Closed')
                ),

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


if __name__ == "__main__":
    initialize_database()
    print("Helpdesk database initialized successfully.")

