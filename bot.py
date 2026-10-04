import os
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes


async def approve_join_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    request = update.chat_join_request

    try:
        await request.approve()
        print(
            f"Approved: "
            f"{request.from_user.username or request.from_user.id}"
        )
    except Exception as e:
        print(f"Error: {e}")


def main():
    token = os.environ["BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(
        ChatJoinRequestHandler(approve_join_request)
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
