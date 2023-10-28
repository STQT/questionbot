from aiogram import Bot


async def check_subscription(bot: Bot, user_id: int, channel_id: str):
    try:
        chat_member = await bot.get_chat_member(channel_id, user_id)
        if chat_member.status in ("member", "administrator", "creator"):
            return True
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False