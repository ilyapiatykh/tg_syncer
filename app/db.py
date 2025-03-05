import sqlite3

DB_URL = "data/tg_syncer.db"


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL)
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS sent_messages (
                    source_message_id INTEGER PRIMARY KEY,
                    target_message_id INTEGER
                );
            """
        )

        self.conn.commit()

    def message_exists(self, source_message_id: str) -> bool:
        self.cursor.execute("SELECT * FROM sent_messages WHERE source_message_id = ?", (source_message_id))
        return self.cursor.fetchone() != None

    def save(self, source_message_id: str, target_message_id: str):
        self.cursor.execute(
            "INSERT INTO sent_messages (source_message_id, target_message_id) VALUES (?, ?)",
            (source_message_id, target_message_id),
        )

        self.conn.commit()

    def get_target_message_id(self, source_message_id: str) -> str | None:
        self.cursor.execute(
            "SELECT target_message_id FROM sent_messages WHERE source_message_id = ?", (source_message_id)
        )
        result = self.cursor.fetchone()

        return result[0] if result else None
        return result[0] if result else None
