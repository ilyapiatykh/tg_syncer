import sqlite3

DB_URL = "data/tg_syncer.db"


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL)
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS sent_messages (
                    target_message_id INTEGER PRIMARY KEY,
                    source_message_id INTEGER,
                    source_channel_id INTEGER,
                    source_message_hash INTEGER
                );
            """
        )

        self.conn.commit()

    def message_exists(
        self,
        source_channel_id: int,
        source_message_hash: int,
    ) -> bool:
        self.cursor.execute(
            "SELECT * FROM sent_messages WHERE source_channel_id = ? AND source_message_hash = ?",
            (source_channel_id, source_message_hash),
        )
        return self.cursor.fetchone() is not None

    def save(
        self,
        source_message_id: int,
        target_message_id: int,
        source_channel_id: int,
        source_message_hash: int,
    ):
        self.cursor.execute(
            "INSERT INTO sent_messages (source_message_id, target_message_id, source_channel_id, source_message_hash) VALUES (?, ?, ?, ?)",
            (
                source_message_id,
                target_message_id,
                source_channel_id,
                source_message_hash,
            ),
        )

        self.conn.commit()

    def get_target_message_id(
        self, source_message_id: int, source_channel_id: int
    ) -> int | None:
        self.cursor.execute(
            "SELECT target_message_id FROM sent_messages WHERE source_message_id = ? AND source_channel_id = ?",
            (source_message_id, source_channel_id),
        )
        result = self.cursor.fetchone()

        return result[0] if result else None
