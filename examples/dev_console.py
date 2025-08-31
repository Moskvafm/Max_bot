import asyncio
from datetime import datetime, timezone

from max_bot.core.types import Update, Message, Chat, User
import examples.simple_bot as app


def make_message_update(text: str, chat_id: int = 1, user_id: int = 100) -> Update:
    msg = Message(
        message_id=int(datetime.now(tz=timezone.utc).timestamp()),
        date=datetime.now(tz=timezone.utc),
        chat=Chat(id=chat_id, type="private"),
        from_user=User(id=user_id),
        text=text,
    )
    return Update(update_id=msg.message_id, message=msg)


def make_callback_update(payload: str, chat_id: int = 1, user_id: int = 100) -> Update:
    # Сначала создаём связанное сообщение для удобства
    msg = Message(
        message_id=int(datetime.now(tz=timezone.utc).timestamp()),
        date=datetime.now(tz=timezone.utc),
        chat=Chat(id=chat_id, type="private"),
        from_user=User(id=user_id),
        text=None,
    )
    # Update с типом callback: api парсер ожидает callback в raw, но здесь формируем напрямую
    from max_bot.core.types import CallbackQuery
    cb = CallbackQuery(id=str(msg.message_id), from_user=msg.from_user, message=msg, data=payload)
    return Update(update_id=msg.message_id, callback_query=cb)


async def main():
    print("Dev console. Введите текст для симуляции сообщения. Команды:")
    print("  /cb <payload>  — симулировать нажатие кнопки с payload")
    print("  /quit          — выход")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line == "/quit":
            break
        if line.startswith("/cb "):
            payload = line[4:].strip()
            upd = make_callback_update(payload)
        else:
            upd = make_message_update(line)
        await app.dp.process_update(upd)


if __name__ == "__main__":
    asyncio.run(main())

