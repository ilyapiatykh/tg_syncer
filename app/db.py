import sqlite3

DB_URL = "data/tg_syncer.db"


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL)
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS sent_messages (
                    id INTEGER AUTO INCREMENT PRIMARY KEY,
                    target_msg_id INTEGER,
                    src_msg_id INTEGER,
                    src_msg_hash TEXT,
                    src_channel_id INTEGER
                );
            """
        )

        self.conn.commit()

    def save(
        self,
        target_msg_id: int,
        src_msg_id: int,
        src_msg_hash: str,
        src_channel_id: int,
    ):
        self.cursor.execute(
            "INSERT INTO sent_messages (target_msg_id, src_msg_id, src_msg_hash, src_channel_id) VALUES (?, ?, ?, ?)",
            (
                target_msg_id,
                src_msg_id,
                src_msg_hash,
                src_channel_id,
            ),
        )

        self.conn.commit()

    def check_duplicate(
        self, src_msg_hash: str, src_channel_id: int
    ) -> int | None:
        self.cursor.execute(
            "SELECT target_msg_id FROM sent_messages WHERE src_msg_hash = ? AND src_channel_id = ?",
            (src_msg_hash, src_channel_id),
        )
        result = self.cursor.fetchone()

        return result[0] if result else None
    
    def get_target_msg_id(
        self, src_msg_id: str, src_channel_id: int
    ) -> int | None:
        self.cursor.execute(
            "SELECT target_msg_id FROM sent_messages WHERE src_msg_id = ? AND src_channel_id = ?",
            (src_msg_id, src_channel_id),
        )
        result = self.cursor.fetchone()

        return result[0] if result else None
