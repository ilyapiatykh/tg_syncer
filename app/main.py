import logging
import re
from typing import Any

from telethon import TelegramClient, events

from app.config import Config
from app.db import DB

TG_SESSION_FILE_PATH = "data/tg_syncer"
LOGFILE_PATH = "data/parser.log"


def remove_binance_line(text: str) -> str:
    return "\n".join(line for line in text.split("\n") if not re.search(r"🆔\s*@binance_360", line)) if text else ""


if __name__ == "__main__":
    config = Config.from_file()

    db = DB()

    logging.basicConfig(filename="data/parser.log", level=logging.INFO, encoding="utf-8")

    with TelegramClient(
        TG_SESSION_FILE_PATH, int(config.api_id.get_secret_value()), config.api_hash.get_secret_value()
    ) as client:

        @client.on(events.NewMessage(chats=config.source_channels_ids))
        async def handler(event: Any):
            try:
                message = event.message

                if not message.text:
                    logging.debug("message without text, skipping.")
                    return

                if db.message_exists(message.id):
                    logging.debug("message was already sent, skipping.")
                    return

                text = remove_binance_line(message.text)

                target_channel = await client.get_input_entity(config.target_channel_id)

                if not message.reply_to_msg_id:
                    sent_message = await client.send_message(target_channel, text)
                    db.save(message.id, sent_message.id)
                    logging.info(f"new message was sent: {text[:20]}...")
                else:
                    replied_message_id = message.reply_to_msg_id
                    target_replied_message_id = db.get_target_message_id(replied_message_id)
                    if not target_replied_message_id:
                        logging.debug(f"no matching message found for reply. ID: {replied_message_id}")

                    sent_message = await client.send_message(target_channel, text, reply_to=target_replied_message_id)
                    db.save(message.id, sent_message.id)
                    logging.info(f"reply was sent: {text[:20]}...")
            except Exception as e:
                logging.exception(f"error processing message: {e}")

        logging.info("script was started")
        client.loop.run_until_complete(client.run_until_disconnected())
