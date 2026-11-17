import json
import time

from sistema import carregar_base, buscar_por_pergunta


def classificar(pergunta, base):
    """Diz o que o assistente faria com a pergunta:
    'VAZIA', 'NENHUM', 'AMBIGUA' ou o id do registro encontrado."""
    if pergunta.strip() == "":
        return "VAZIA"
    encontrados, _ = buscar_por_pergunta(pergunta, base)
    if len(encontrados) == 0:
        return "NENHUM"
    if len(encontrados) > 1:
        return "AMBIGUA"
    return encontrados[0]["id"]


def main():
    base = carregar_base("data/base_conhecimento.json")
    perguntas = carregar_base("data/perguntas_teste.json")
    if base is None or perguntas is None:
        return

    resultados = []
    acertos = 0
    soma_tempos = 0.0

    print(f"{'Nº':>2} | {'Pergunta':<30} | {'Esperado':<10} | {'Obtido':<10} | {'Resultado':<9} | Tempo")
    print("-" * 85)

    for numero, item in enumerate(perguntas, start=1):
        inicio = time.perf_counter()
        obtido = classificar(item["pergunta"], base)
        tempo_ms = (time.perf_counter() - inicio) * 1000

        acertou = obtido == item["esperado"]
        if acertou:
            acertos += 1
        soma_tempos += tempo_ms

        texto = item["pergunta"] if item["pergunta"] != "" else "(vazia)"
        marca = "ACERTO" if acertou else "ERRO"
        print(f"{numero:>2} | {texto[:30]:<30} | {item['esperado']:<10} | {obtido:<10} | {marca:<9} | {tempo_ms:.4f} ms")

        resultados.append({
            "pergunta": item["pergunta"],
            "tipo": item["tipo"],
            "esperado": item["esperado"],
            "obtido": obtido,
            "resultado": marca,
            "tempo_ms": round(tempo_ms, 4),
        })

    total = len(perguntas)
    taxa = acertos / total * 100
    media = soma_tempos / total

    print("-" * 85)
    print(f"Perguntas testadas: {total}")
    print(f"Acertos: {acertos}")
    print(f"Taxa de acerto: {taxa:.1f}%")
    print(f"Tempo médio de consulta: {media:.4f} ms")

    # Salva o registro dos resultados
    with open("data/resultados_testes.json", "w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, ensure_ascii=False, indent=2)
    print("Resultados salvos em data/resultados_testes.json")


if __name__ == "__main__":
    main()