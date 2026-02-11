from telegram import Update
from telegram.ext import ContextTypes
from bot.storage import load_data, save_data
from bot.logic import avaliar_status

async def km(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /km <km_atual>")
        return

    try:
        km_atual = int(context.args[0])
    except ValueError:
        await update.message.reply_text("O KM deve ser um número inteiro.")
        return

    data = load_data()
    msgs = avaliar_status(km_atual, data)
    await update.message.reply_text("\n".join(msgs))

async def abastecer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /abastecer <km>")
        return

    try:
        km = int(context.args[0])
    except ValueError:
        await update.message.reply_text("O KM deve ser um número inteiro.")
        return

    data = load_data()
    data["ultimo_abastecimento"] = km
    save_data(data)
    await update.message.reply_text(f"⛽ Abastecimento registrado em {km} km.")

async def oleo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /oleo <km>")
        return

    try:
        km = int(context.args[0])
    except ValueError:
        await update.message.reply_text("O KM deve ser um número inteiro.")
        return

    data = load_data()
    data["ultimo_oleo"] = km
    save_data(data)
    await update.message.reply_text(f"🛢️ Troca de óleo registrada em {km} km.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /status <km_atual>")
        return

    try:
        km_atual = int(context.args[0])
    except ValueError:
        await update.message.reply_text("O KM deve ser um número inteiro.")
        return

    data = load_data()
    msgs = avaliar_status(km_atual, data)
    await update.message.reply_text("\n".join(msgs))
