import logging
from aiogram import types, Bot

async def _delete_and_send(bot: Bot, chat_id: int, message_id: int, text: str, **kwargs):
    """Delete previous message and send a new one."""
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        # Deleting might fail if message is already gone; log for debugging
        logging.debug(
            "Failed to delete message %s in chat %s: %s", message_id, chat_id, e
        )
    return await bot.send_message(chat_id=chat_id, text=text, **kwargs)

async def patched_message_edit_text(self: types.Message, text: str, **kwargs):
    """Patch for Message.edit_text to delete old message and send new one."""
    new_message = await _delete_and_send(
        bot=self.bot,
        chat_id=self.chat.id,
        message_id=self.message_id,
        text=text,
        **kwargs,
    )
    # Update current message object to reflect new message
    self.__dict__.update(new_message.__dict__)
    return new_message

async def patched_bot_edit_message_text(
    self: Bot, *, chat_id: int, message_id: int, text: str, **kwargs
):
    """Patch for Bot.edit_message_text to delete before sending new message."""
    return await _delete_and_send(
        bot=self,
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        **kwargs,
    )

def patch_edit_message() -> None:
    """Apply patches to edit methods so updates send new messages instead."""
    types.Message.edit_text = patched_message_edit_text
    Bot.edit_message_text = patched_bot_edit_message_text
