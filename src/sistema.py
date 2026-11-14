import json
import re
import unicodedata

# Campos que todo registro da base precisa ter
CAMPOS_OBRIGATORIOS = [
    "id", "tema", "palavras_chave",
    "orientacao", "referencia", "data_verificacao",
]

# Grafo simples: cada tema aponta para os temas ligados a ele
RELACIONADOS = {
    "trabalho":      ["educacao", "consumidor", "transito"],
    "educacao":      ["trabalho", "meio_ambiente"],
    "transito":      ["consumidor", "trabalho"],
    "meio_ambiente": ["consumidor", "educacao"],
    "consumidor":    ["transito", "meio_ambiente", "trabalho"],
}

# Modelo de resposta em uso: "A" (curto) ou "B" (detalhado)
MODELO_ATUAL = {"nome": "B"}

def carregar_base(caminho):
    """Lê o arquivo JSON e devolve uma lista de dicionários.
    Se der problema, avisa e devolve None."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print(f"Erro: o arquivo '{caminho}' não foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: o arquivo '{caminho}' está vazio ou mal escrito.")
        print("Confira vírgulas, aspas duplas e colchetes no JSON.")
    return None


def validar_base(base):
    """Confere se a base tem registros e se todos têm os campos obrigatórios.
    Devolve uma lista de problemas (lista vazia = base válida)."""
    problemas = []

    if not isinstance(base, list) or len(base) == 0:
        problemas.append("A base está vazia ou não é uma lista de registros.")
        return problemas

    for posicao, registro in enumerate(base, start=1):
        if not isinstance(registro, dict):
            problemas.append(f"Registro {posicao}: formato inválido.")
            continue
        for campo in CAMPOS_OBRIGATORIOS:
            if campo not in registro:
                problemas.append(f"Registro {posicao}: falta o campo '{campo}'.")
                continue
            valor = registro[campo]
            vazio = valor is None or valor == [] or (
                isinstance(valor, str) and valor.strip() == ""
            )
            if vazio:
                problemas.append(f"Registro {posicao}: o campo '{campo}' está em branco.")

    return problemas


def listar_temas(base):
    """Devolve os temas da base, sem repetir."""
    temas = []
    for registro in base:
        if registro["tema"] not in temas:
            temas.append(registro["tema"])
    return temas


def ler_numero(texto, maximo, minimo=1):
    """Pede um número de 'minimo' até 'maximo'. Se for inválido, avisa e devolve None."""
    entrada = input(texto).strip()
    if entrada == "":
        print("Você não digitou nada.")
        return None
    try:
        numero = int(entrada)
    except ValueError:
        print("Digite apenas números.")
        return None
    if numero < minimo or numero > maximo:
        print(f"Opção inexistente. Escolha um número de {minimo} a {maximo}.")
        return None
    return numero

def mostrar_orientacao(registro):
    """Mostra a orientação usando o modelo de resposta atual."""
    print("\n--- Orientação ---")
    if MODELO_ATUAL["nome"] == "A":
        print(formatar_modelo_a(registro))
    else:
        print(formatar_modelo_b(registro))

def consultar_por_tema(base):
    """Escolhe um tema e começa a navegação a partir dele."""
    temas = listar_temas(base)
    print("\nTemas disponíveis:")
    for numero, tema in enumerate(temas, start=1):
        print(f"{numero}. {tema}")

    escolha = ler_numero("Escolha um tema: ", len(temas))
    if escolha is None:
        return
    navegar(base, temas[escolha - 1])

def normalizar(texto):
    """Deixa o texto em minúsculas, sem acentos e sem pontuação.
    Ex.: 'Como tiro a Segunda Via do RG?' -> 'como tiro a segunda via do rg'"""
    texto = texto.lower()
    # Separa a letra do acento e descarta o acento
    texto = unicodedata.normalize("NFD", texto)
    sem_acento = ""
    for letra in texto:
        if unicodedata.category(letra) != "Mn":
            sem_acento += letra
    # Troca qualquer coisa que não seja letra, número ou espaço por espaço
    sem_acento = re.sub(r"[^a-z0-9 ]", " ", sem_acento)
    return " ".join(sem_acento.split())


def pontuar(pergunta_norm, registro):
    """Conta quantas palavras-chave do registro aparecem na pergunta."""
    pontos = 0
    for palavra in registro["palavras_chave"]:
        # Os espaços nas pontas evitam achar 'rg' dentro de 'energia'
        if f" {normalizar(palavra)} " in f" {pergunta_norm} ":
            pontos += 1
    return pontos


def buscar_por_pergunta(pergunta, base):
    """Devolve (lista de melhores registros, pontuação).
    Se houver empate, devolve todos os empatados. Se nada pontuar, lista vazia."""
    pergunta_norm = normalizar(pergunta)
    melhor_pontuacao = 0
    melhores = []
    for registro in base:
        pontos = pontuar(pergunta_norm, registro)
        if pontos > melhor_pontuacao:
            melhor_pontuacao = pontos
            melhores = [registro]
        elif pontos == melhor_pontuacao and pontos > 0:
            melhores.append(registro)
    return melhores, melhor_pontuacao


def consultar_por_pergunta(base):
    """Pede uma pergunta, busca na base e mostra a resposta ou um aviso."""
    pergunta = input("\nDigite sua pergunta: ")
    if pergunta.strip() == "":
        print("Você não digitou nada.")
            # Depois da resposta, oferece continuar por temas relacionados
    proximo = oferecer_relacionados(base, encontrados[0]["tema"])
    if proximo is not None:
        navegar(base, proximo)
        return

    encontrados, pontos = buscar_por_pergunta(pergunta, base)

    if not encontrados:
        print("Não encontrei uma orientação sobre isso na base.")
        print("Tente outras palavras ou escolha um tema:", ", ".join(listar_temas(base)))
        return

    mostrar_orientacao(encontrados[0])
    # Se houve empate, mostra as outras possibilidades
    if len(encontrados) > 1:
        print("\nTambém encontrei estas orientações parecidas:")
        for registro in encontrados[1:]:
            print(f"- {registro['id']} ({registro['tema']}): {', '.join(registro['palavras_chave'])}")

def temas_relacionados(tema):
    """Devolve a lista de temas ligados a 'tema' no grafo."""
    return RELACIONADOS.get(tema, [])


def escolher_orientacao_do_tema(base, tema):
    """Lista as orientações de um tema, deixa escolher uma e mostra.
    Devolve True se mostrou uma orientação."""
    registros_do_tema = []
    for registro in base:
        if registro["tema"] == tema:
            registros_do_tema.append(registro)

    print(f"\nOrientações sobre {tema}:")
    for numero, registro in enumerate(registros_do_tema, start=1):
        print(f"{numero}. {registro['id']} - {', '.join(registro['palavras_chave'])}")

    escolha = ler_numero("Escolha uma orientação: ", len(registros_do_tema))
    if escolha is None:
        return False
    mostrar_orientacao(registros_do_tema[escolha - 1])
    return True


def oferecer_relacionados(base, tema):
    """Mostra os temas ligados a 'tema' que existem na base.
    Devolve o tema escolhido, ou None se o usuário quiser voltar."""
    existentes = listar_temas(base)
    opcoes = []
    for t in temas_relacionados(tema):
        if t in existentes:          # só oferece temas que têm registros
            opcoes.append(t)

    if not opcoes:
        return None

    print("\nAssuntos relacionados:")
    for numero, t in enumerate(opcoes, start=1):
        print(f"{numero}. {t}")
    print("0. Voltar ao menu")

    escolha = ler_numero("Quer continuar por outro assunto? ", len(opcoes), minimo=0)
    if escolha is None or escolha == 0:
        return None
    return opcoes[escolha - 1]


def navegar(base, tema):
    """Mostra uma orientação e segue oferecendo temas relacionados,
    até o usuário voltar ao menu."""
    while tema is not None:
        if not escolher_orientacao_do_tema(base, tema):
            return
        tema = oferecer_relacionados(base, tema)

def formatar_modelo_a(registro):
    """MODELO A (curto e direto)
    Papel: assistente objetivo, que responde em poucas linhas.
    Formato: orientação + fonte + lembrete curto.
    Regra: sempre citar a fonte."""
    return (
        f"{registro['orientacao']}\n"
        f"Fonte: {registro['referencia']}\n"
        "Confirme na fonte oficial."
    )


def formatar_modelo_b(registro):
    """MODELO B (detalhado)
    Papel: assistente de orientação cidadã, não oficial.
    Formato: tema, orientação, fonte, data de verificação e aviso.
    Regra: sempre citar a fonte e avisar que é preciso confirmar."""
    return (
        "Assistente de orientação cidadã (informação não oficial)\n"
        f"Tema: {registro['tema']}\n"
        f"Orientação: {registro['orientacao']}\n"
        f"Fonte consultada: {registro['referencia']}\n"
        f"Verificado em: {registro['data_verificacao']}\n"
        "Atenção: as regras podem mudar. Confirme no site oficial antes de agir. "
        "Este assistente não é um canal oficial de órgãos públicos."
    )


def alternar_modelo():
    """Troca entre o modelo A e o modelo B."""
    if MODELO_ATUAL["nome"] == "A":
        MODELO_ATUAL["nome"] = "B"
    else:
        MODELO_ATUAL["nome"] = "A"
    print(f"Modelo de resposta alterado para {MODELO_ATUAL['nome']}.")

def main():
    """Carrega e valida a base, depois mostra o menu até o usuário sair."""
    base = carregar_base("data/base_conhecimento.json")
    if base is None:
        print("Não foi possível iniciar o assistente.")
        return

    problemas = validar_base(base)
    if problemas:
        print("A base de conhecimento tem problemas:")
        for problema in problemas:
            print(" -", problema)
        print("Corrija o arquivo e execute novamente.")
        return

    while True:
        print("\n=== Citizen Assist AI ===")
        print("1. Ver temas disponíveis")
        print("2. Consultar por tema")
        print("3. Fazer uma pergunta")
        print(f"4. Trocar modelo de resposta (atual: {MODELO_ATUAL['nome']})")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            for numero, tema in enumerate(listar_temas(base), start=1):
                print(f"{numero}. {tema}")
        elif opcao == "2":
            consultar_por_tema(base)
        elif opcao == "3":
            consultar_por_pergunta(base)
        elif opcao == "4":
            alternar_modelo()
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Digite 1, 2, 3, 4 ou 0.")


main()