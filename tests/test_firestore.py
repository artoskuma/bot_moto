print("COMEÇOU")

from bot.storage import salvar_abastecimento

print("ANTES DE SALVAR")
salvar_abastecimento(123, {"ok": True})
print("TERMINOU")
