import os
from telegram.ext import Application, CommandHandler
from bot.handlers import km, abastecer, oleo, status

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN não encontrado")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("km", km))
    app.add_handler(CommandHandler("abastecer", abastecer))
    app.add_handler(CommandHandler("oleo", oleo))
    app.add_handler(CommandHandler("status", status))

    app.run_polling(stop_signals=None)

if __name__ == "__main__":
    main()
