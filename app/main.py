import re
from hashlib import sha256
from typing import Any

from loguru import logger
from telethon import TelegramClient, events

from app.config import Config
from app.db import DB

TG_SESSION_FILE_PATH = "data/tg_syncer"
LOGFILE_PATH = "data/tg_syncer.log"


def format_text(text: str) -> str:
    return re.sub(r"🆔\s*@binance_360", "", text)


def hash_text(text: str) -> str:
    return sha256(text.encode()).hexdigest()


if __name__ == "__main__":
    config = Config.from_file()

    db = DB()

    logger.add(LOGFILE_PATH)

    with TelegramClient(
        TG_SESSION_FILE_PATH,
        int(config.api_id.get_secret_value()),
        config.api_hash.get_secret_value(),
    ) as client:

        @client.on(events.NewMessage(chats=config.source_channels_ids))
        @logger.catch(
            Exception,
            message="failed to process new message",
            reraise=False,
            level="ERROR",
        )
        async def handler(event: Any):
            src_msg = event.message
            src_channel_id = event.chat_id

            with logger.contextualize(
                channel=src_channel_id, msg_id=src_msg.id, text=src_msg.text
            ):
                logger.debug("new message")

                if not src_msg.text:
                    logger.debug("message without text, skip")
                    return

                text = format_text(src_msg.text)
                msg_hash = hash_text(text)

                target_msg_id = db.check_duplicate(msg_hash, src_channel_id)

                if target_msg_id:
                    db.save(
                        target_msg_id, src_msg.id, msg_hash, src_channel_id
                    )
                    logger.debug("save message duplicate and skip")
                    return

                target_channel = await client.get_input_entity(
                    config.target_channel_id
                )

                target_replied_msg_id = None
                if src_msg.reply_to_msg_id:
                    target_replied_msg_id = db.get_target_msg_id(
                        src_msg.reply_to_msg_id, src_channel_id
                    )
                    if not target_replied_msg_id:
                        logger.warning("no matching message found for reply")
                        return

                sent_message = await client.send_message(
                    target_channel, text, reply_to=target_replied_msg_id
                )

                db.save(
                    sent_message.id,
                    src_msg.id,
                    msg_hash,
                    src_channel_id,
                )

                logger.info("new message was sent")

        logger.info("script was started")
        client.loop.run_until_complete(client.run_until_disconnected())
