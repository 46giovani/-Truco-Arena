import random

# ==========================================
# CONFIGURAÇÕES
# ==========================================

NAIPES = ["Paus", "Copas", "Espadas", "Ouros"]
VALORES = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]

ORDEM = {
    "4": 1,
    "5": 2,
    "6": 3,
    "7": 4,
    "Q": 5,
    "J": 6,
    "K": 7,
    "A": 8,
    "2": 9,
    "3": 10
}

# Ordem dos naipes para desempate das manilhas
ORDEM_NAIPES = {
    "Ouros": 1,
    "Espadas": 2,
    "Copas": 3,
    "Paus": 4
}


# ==========================================
# CARTA
# ==========================================

class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def __str__(self):
        simbolos = {
            "Paus": "♣",
            "Copas": "♥",
            "Espadas": "♠",
            "Ouros": "♦"
        }

        return f"{self.valor}{simbolos[self.naipe]}"


# ==========================================
# BARALHO
# ==========================================

def criar_baralho():
    baralho = []

    for valor in VALORES:
        for naipe in NAIPES:
            baralho.append(Carta(valor, naipe))

    return baralho


# ==========================================
# VALOR DA CARTA
# ==========================================

def valor_carta(carta, vira):
    """
    Retorna a força da carta.
    Se a carta for uma manilha, recebe valor superior.
    """

    # Descobre qual é a manilha
    indice = VALORES.index(vira.valor)

    if indice + 1 >= len(VALORES):
        manilha = VALORES[0]
    else:
        manilha = VALORES[indice + 1]

    # Manilhas são sempre mais fortes
    if carta.valor == manilha:
        return 100 + ORDEM_NAIPES[carta.naipe]

    return ORDEM[carta.valor]


# ==========================================
# MOSTRAR CARTAS
# ==========================================

def mostrar_cartas(cartas):
    for i, carta in enumerate(cartas):
        print(f"[{i + 1}] {carta}", end="   ")

    print()


# ==========================================
# ESCOLHER CARTA DO JOGADOR
# ==========================================

def escolher_carta(jogador):
    while True:
        try:
            escolha = int(input("\nEscolha uma carta: "))

            if 1 <= escolha <= len(jogador):
                return jogador.pop(escolha - 1)

            print("Escolha uma carta válida.")

        except ValueError:
            print("Digite apenas um número.")


# ==========================================
# COMPUTADOR ESCOLHE CARTA
# ==========================================

def computador_escolhe_carta(computador, vira, carta_adversaria=None):

    # Se já existe uma carta adversária,
    # tenta jogar uma carta que vença.
    if carta_adversaria:

        cartas_que_vencem = []

        for carta in computador:
            if valor_carta(carta, vira) > valor_carta(carta_adversaria, vira):
                cartas_que_vencem.append(carta)

        if cartas_que_vencem:
            carta = min(
                cartas_que_vencem,
                key=lambda c: valor_carta(c, vira)
            )

            computador.remove(carta)
            return carta

    # Caso contrário, joga uma carta aleatória
    carta = random.choice(computador)
    computador.remove(carta)

    return carta


# ==========================================
# TRUCO
# ==========================================

def pedir_truco(pontos_rodada):

    print("\n================================")
    print("        O COMPUTADOR PEDIU TRUCO!")
    print("================================")

    while True:

        print("\nValor atual da rodada:", pontos_rodada)
        print("[1] Aceitar")
        print("[2] Pedir 6")
        print("[3] Recusar")

        escolha = input("Sua escolha: ")

        if escolha == "1":
            return pontos_rodada

        elif escolha == "2":

            if pontos_rodada == 3:
                return 6

            elif pontos_rodada == 6:
                return 9

            elif pontos_rodada == 9:
                return 12

            else:
                print("Não é possível aumentar agora.")

        elif escolha == "3":
            return 0

        else:
            print("Opção inválida.")


# ==========================================
# COMPUTADOR DECIDE PEDIR TRUCO
# ==========================================

def computador_pede_truco(pontos_rodada, carta):

    forca = ORDEM[carta.valor]

    # Manilha
    if forca >= 100:
        if pontos_rodada < 12:
            return True

    # Cartas muito fortes
    if carta.valor in ["3", "2", "A"]:
        if pontos_rodada <= 3:
            return random.choice([True, False])

    return False


# ==========================================
# JOGAR RODADA
# ==========================================

def jogar_rodada(jogador, computador, vira):

    cartas_jogador = []
    cartas_computador = []

    for _ in range(3):
        cartas_jogador.append(jogador.pop())
        cartas_computador.append(computador.pop())

    pontos_rodada = 1

    vitorias_jogador = 0
    vitorias_computador = 0

    print("\n====================================")
    print("          NOVA MÃO")
    print("====================================")

    print(f"Vira: {vira}")
    print("Sua mão:")
    mostrar_cartas(cartas_jogador)

    print("\nManilha será o valor seguinte à vira.")

    # ==========================================
    # 3 VAZAS
    # ==========================================

    for numero_vaza in range(1, 4):

        print("\n------------------------------------")
        print(f"             VAZA {numero_vaza}")
        print("------------------------------------")

        print("\nSuas cartas:")
        mostrar_cartas(cartas_jogador)

        # Jogador joga
        carta_jogador = escolher_carta(cartas_jogador)

        print(f"\nVocê jogou: {carta_jogador}")

        # Computador joga
        carta_computador = computador_escolhe_carta(
            cartas_computador,
            vira,
            carta_jogador
        )

        print(f"Computador jogou: {carta_computador}")

        valor_jogador = valor_carta(carta_jogador, vira)
        valor_computador = valor_carta(carta_computador, vira)

        # ==========================================
        # VERIFICAR VENCEDOR
        # ==========================================

        if valor_jogador > valor_computador:

            print("\nVocê ganhou a vaza!")
            vitorias_jogador += 1

        elif valor_computador > valor_jogador:

            print("\nO computador ganhou a vaza!")
            vitorias_computador += 1

        else:

            print("\nEmpate!")

            # Em empate, quem venceu a anterior
            # normalmente leva vantagem.
            if vitorias_jogador > vitorias_computador:
                vitorias_jogador += 1

            elif vitorias_computador > vitorias_jogador:
                vitorias_computador += 1

        print(
            f"\nVazas: Você {vitorias_jogador} x "
            f"{vitorias_computador} Computador"
        )

        # ==========================================
        # COMPUTADOR PODE PEDIR TRUCO
        # ==========================================

        if numero_vaza < 3 and cartas_computador:

            ultima_carta = cartas_computador[0]

            if computador_pede_truco(pontos_rodada, ultima_carta):

                if pontos_rodada == 1:
                    print("\nO computador pediu TRUCO!")

                elif pontos_rodada == 3:
                    print("\nO computador pediu 6!")

                elif pontos_rodada == 6:
                    print("\nO computador pediu 9!")

                elif pontos_rodada == 9:
                    print("\nO computador pediu 12!")

                novo_valor = pedir_truco(pontos_rodada)

                if novo_valor == 0:

                    print("\nVocê recusou.")

                    return "computador", pontos_rodada

                pontos_rodada = novo_valor

        # ==========================================
        # JOGADOR PODE PEDIR TRUCO
        # ==========================================

        if numero_vaza < 3 and pontos_rodada < 12:

            resposta = input(
                "\nQuer pedir Truco/Aumentar? "
                "(s/n): "
            ).lower()

            if resposta == "s":

                if pontos_rodada == 1:
                    novo_valor = 3
                elif pontos_rodada == 3:
                    novo_valor = 6
                elif pontos_rodada == 6:
                    novo_valor = 9
                else:
                    novo_valor = 12

                print(f"\nVocê pediu {novo_valor}!")

                # Computador decide
                aceitar = random.choice([True, True, False])

                if not aceitar:

                    print("O computador recusou!")

                    return "jogador", pontos_rodada

                print("O computador aceitou!")

                pontos_rodada = novo_valor

        # ==========================================
        # VERIFICAR SE ALGUÉM JÁ GANHOU
        # ==========================================

        if vitorias_jogador >= 2:

            return "jogador", pontos_rodada

        if vitorias_computador >= 2:

            return "computador", pontos_rodada

    # ==========================================
    # RESULTADO DA MÃO
    # ==========================================

    if vitorias_jogador > vitorias_computador:
        return "jogador", pontos_rodada

    elif vitorias_computador > vitorias_jogador:
        return "computador", pontos_rodada

    else:
        return "empate", pontos_rodada


# ==========================================
# JOGO PRINCIPAL
# ==========================================

def jogar():

    pontos_jogador = 0
    pontos_computador = 0

    print("==========================================")
    print("             TRUCO PAULISTA")
    print("==========================================")

    print("\nPrimeiro jogador a chegar em 12 pontos vence!")

    while pontos_jogador < 12 and pontos_computador < 12:

        print("\n==========================================")
        print("                PLACAR")
        print("==========================================")

        print(f"Você:       {pontos_jogador}")
        print(f"Computador: {pontos_computador}")

        # Criar e embaralhar baralho
        baralho = criar_baralho()
        random.shuffle(baralho)

        # Distribuir cartas
        jogador = []
        computador = []

        for _ in range(3):
            jogador.append(baralho.pop())

        for _ in range(3):
            computador.append(baralho.pop())

        # Vira
        vira = baralho.pop()

        print(f"\nVira: {vira}")

        # Jogar mão
        vencedor, pontos = jogar_rodada(
            jogador,
            computador,
            vira
        )

        # ==========================================
        # ATUALIZAR PLACAR
        # ==========================================

        if vencedor == "jogador":

            pontos_jogador += pontos

            print("\n================================")
            print("       VOCÊ GANHOU A MÃO!")
            print(f"       +{pontos} pontos")
            print("================================")

        elif vencedor == "computador":

            pontos_computador += pontos

            print("\n================================")
            print("    COMPUTADOR GANHOU A MÃO!")
            print(f"       +{pontos} pontos")
            print("================================")

        else:

            print("\nA mão terminou empatada.")

        # ==========================================
        # PAUSA
        # ==========================================

        input("\nPressione ENTER para continuar...")

    # ==========================================
    # FIM DO JOGO
    # ==========================================

    print("\n==========================================")
    print("              FIM DO JOGO")
    print("==========================================")

    print(f"\nVocê:       {pontos_jogador}")
    print(f"Computador: {pontos_computador}")

    if pontos_jogador >= 12:

        print("\nPARABÉNS! VOCÊ VENCEU O JOGO!")

    else:

        print("\nO COMPUTADOR VENCEU O JOGO!")

    print("\nObrigado por jogar!")


# ==========================================
# INICIAR
# ==========================================

if __name__ == "__main__":
    jogar()