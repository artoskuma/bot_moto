import os
import json
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# TOKEN do bot vindo das Environment Variables do Render
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN não encontrado no Render")

# Arquivo para salvar dados
DATA_FILE = Path("dados.json")
if not DATA_FILE.exists():
    DATA_FILE.write_text("{}")  # Cria vazio se não existir

# Configurações
AVISO_ANTECIPADO = 125
AVISO_CRITICO = 145
AVISO_ESTOURADO = 152
INTERVALO_OLEO = 1000

# --- Funções auxiliares ---
def load_data():
    return json.loads(DATA_FILE.read_text())

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

def avaliar_status(km_atual: int, data: dict) -> list[str]:
    msgs = []

    # Combustível
    if "ultimo_abastecimento" in data:
        rodado = km_atual - data["ultimo_abastecimento"]
        msgs.append(f"⛽ KM desde abastecimento: {rodado} km")

        if rodado >= AVISO_ESTOURADO:
            msgs.append("🛑 Reserva estourada — abasteça imediatamente")
        elif rodado >= AVISO_CRITICO:
            msgs.append("🚨 Provável reserva — planeje abastecer")
        elif rodado >= AVISO_ANTECIPADO:
            msgs.append("⚠️ Atenção: aproximando da reserva")
        else:
            msgs.append("✅ Combustível ok")
    else:
        msgs.append("⛽ Nenhum abastecimento registrado.")

    # Óleo
    if "ultimo_oleo" in data:
        rodado_oleo = km_atual - data["ultimo_oleo"]
        faltam = INTERVALO_OLEO - rodado_oleo
        msgs.append(f"\n🛢️ KM desde troca de óleo: {rodado_oleo} km")
        msgs.append(f"Próxima troca em: {faltam} km")

        if rodado_oleo >= INTERVALO_OLEO - 100:
            msgs.append("⚠️ Atenção: troca de óleo se aproximando")
    else:
        msgs.append("\n🛢️ Nenhuma troca de óleo registrada.")

    return msgs

# --- Comandos do bot ---
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

# --- Inicialização do bot ---
def main():
    print("Iniciando bot...")  # Útil para ver logs no Render
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("km", km))
    app.add_handler(CommandHandler("abastecer", abastecer))
    app.add_handler(CommandHandler("oleo", oleo))
    app.add_handler(CommandHandler("status", status))

    app.run_polling()

if __name__ == "__main__":
    main()
