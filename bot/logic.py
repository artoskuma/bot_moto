AVISO_ANTECIPADO = 125
AVISO_CRITICO = 145
AVISO_ESTOURADO = 152
INTERVALO_OLEO = 1000

def avaliar_status(km_atual: int, data: dict) -> list[str]:
    msgs = []

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
