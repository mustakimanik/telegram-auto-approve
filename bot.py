import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass


def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    threading.Thread(target=start_web_server, daemon=True).start()

    token = os.environ["BOT_TOKEN"]

    app = Application.builder().token(token).build()
    app.add_handler(ChatJoinRequestHandler(approve_join_request))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
