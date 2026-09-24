import pygame
import random
import sys

pygame.init()

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

LARGURA, ALTURA = 1100, 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Truco Paulista")

FPS = 60
FONTE = pygame.font.SysFont("Arial", 24)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 18)
FONTE_GRANDE = pygame.font.SysFont("Arial", 36, bold=True)

FUNDO = (25, 100, 55)
FUNDO_ESCURO = (15, 65, 35)
BRANCO = (245, 245, 245)
PRETO = (20, 20, 20)
CINZA = (190, 190, 190)
VERMELHO = (180, 35, 35)
DOURADO = (235, 190, 60)

BOTAO = (55, 55, 65)
BOTAO_HOVER = (80, 80, 95)

NAIPES = ["Paus", "Copas", "Espadas", "Ouros"]

VALORES = [
    "4", "5", "6", "7",
    "Q", "J", "K", "A",
    "2", "3"
]

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

ORDEM_NAIPES = {
    "Ouros": 1,
    "Espadas": 2,
    "Copas": 3,
    "Paus": 4
}

SIMBOLOS = {
    "Paus": "♣",
    "Copas": "♥",
    "Espadas": "♠",
    "Ouros": "♦"
}


# ==========================================================
# CARTA
# ==========================================================

class Carta:

    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def __str__(self):
        return f"{self.valor}{SIMBOLOS[self.naipe]}"


# ==========================================================
# BARALHO
# ==========================================================

def criar_baralho():

    baralho = []

    for valor in VALORES:

        for naipe in NAIPES:

            baralho.append(
                Carta(valor, naipe)
            )

    return baralho


# ==========================================================
# VALOR DA CARTA
# ==========================================================

def valor_carta(carta, vira):

    indice = VALORES.index(vira.valor)

    manilha = VALORES[
        (indice + 1) % len(VALORES)
    ]

    if carta.valor == manilha:

        return 100 + ORDEM_NAIPES[carta.naipe]

    return ORDEM[carta.valor]


# ==========================================================
# TEXTO DA CARTA
# ==========================================================

def texto_carta(carta):

    return f"{carta.valor} {SIMBOLOS[carta.naipe]}"


# ==========================================================
# DESENHAR TEXTO
# ==========================================================

def desenhar_texto(
    texto,
    x,
    y,
    fonte=FONTE,
    cor=BRANCO,
    centralizado=False
):

    imagem = fonte.render(
        texto,
        True,
        cor
    )

    rect = imagem.get_rect()

    if centralizado:

        rect.center = (x, y)

    else:

        rect.topleft = (x, y)

    TELA.blit(
        imagem,
        rect
    )

    return rect


# ==========================================================
# BOTÃO
# ==========================================================

def desenhar_botao(
    rect,
    texto
):

    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):

        cor = BOTAO_HOVER

    else:

        cor = BOTAO

    pygame.draw.rect(
        TELA,
        cor,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        TELA,
        BRANCO,
        rect,
        2,
        border_radius=10
    )

    desenhar_texto(
        texto,
        rect.centerx,
        rect.centery,
        FONTE_PEQUENA,
        BRANCO,
        True
    )


# ==========================================================
# DESENHAR CARTA
# ==========================================================

def desenhar_carta(
    carta,
    rect,
    selecionada=False
):

    pygame.draw.rect(
        TELA,
        BRANCO,
        rect,
        border_radius=10
    )

    if selecionada:

        borda = DOURADO

    else:

        borda = PRETO

    pygame.draw.rect(
        TELA,
        borda,
        rect,
        3,
        border_radius=10
    )

    if carta.naipe in [
        "Copas",
        "Ouros"
    ]:

        cor = VERMELHO

    else:

        cor = PRETO

    fonte = pygame.font.SysFont(
        "Arial",
        28,
        bold=True
    )

    desenhar_texto(
        texto_carta(carta),
        rect.centerx,
        rect.centery - 5,
        fonte,
        cor,
        True
    )

    fonte_naipe = pygame.font.SysFont(
        "Arial",
        13
    )

    desenhar_texto(
        carta.naipe,
        rect.centerx,
        rect.bottom - 18,
        fonte_naipe,
        cor,
        True
    )


# ==========================================================
# DESENHAR MÃO
# ==========================================================

def desenhar_mao(
    cartas,
    y,
    selecionada=-1
):

    largura = 145
    altura = 100
    espacamento = 25

    total = (
        len(cartas) * largura
        + max(
            0,
            len(cartas) - 1
        ) * espacamento
    )

    x = (
        LARGURA - total
    ) // 2

    rects = []

    for i, carta in enumerate(cartas):

        rect = pygame.Rect(
            x + i * (
                largura + espacamento
            ),
            y,
            largura,
            altura
        )

        desenhar_carta(
            carta,
            rect,
            i == selecionada
        )

        rects.append(rect)

    return rects


# ==========================================================
# TELA DE TRUCO
# ==========================================================

def tela_truco(pontos):

    clock = pygame.time.Clock()

    while True:

        TELA.fill(FUNDO)

        desenhar_texto(
            "O COMPUTADOR PEDIU TRUCO!",
            LARGURA // 2,
            180,
            FONTE_GRANDE,
            BRANCO,
            True
        )

        desenhar_texto(
            f"Valor atual: {pontos}",
            LARGURA // 2,
            240,
            FONTE,
            BRANCO,
            True
        )

        aceitar = pygame.Rect(
            220,
            330,
            180,
            60
        )

        aumentar = pygame.Rect(
            460,
            330,
            180,
            60
        )

        recusar = pygame.Rect(
            700,
            330,
            180,
            60
        )

        desenhar_botao(
            aceitar,
            "ACEITAR"
        )

        desenhar_botao(
            aumentar,
            "AUMENTAR"
        )

        desenhar_botao(
            recusar,
            "RECUSAR"
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if (
                evento.type
                == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):

                if aceitar.collidepoint(
                    evento.pos
                ):

                    return pontos

                if aumentar.collidepoint(
                    evento.pos
                ):

                    if pontos == 3:
                        return 6

                    if pontos == 6:
                        return 9

                    if pontos == 9:
                        return 12

                if recusar.collidepoint(
                    evento.pos
                ):

                    return 0

        pygame.display.flip()

        clock.tick(FPS)


# ==========================================================
# TRUCO DO JOGADOR
# ==========================================================

def perguntar_truco_jogador(
    pontos
):

    clock = pygame.time.Clock()

    while True:

        TELA.fill(FUNDO)

        desenhar_texto(
            "QUER PEDIR TRUCO?",
            LARGURA // 2,
            190,
            FONTE_GRANDE,
            BRANCO,
            True
        )

        desenhar_texto(
            f"Valor atual: {pontos}",
            LARGURA // 2,
            245,
            FONTE,
            BRANCO,
            True
        )

        sim = pygame.Rect(
            300,
            330,
            200,
            60
        )

        nao = pygame.Rect(
            600,
            330,
            200,
            60
        )

        desenhar_botao(
            sim,
            "SIM"
        )

        desenhar_botao(
            nao,
            "NÃO"
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if (
                evento.type
                == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):

                if sim.collidepoint(
                    evento.pos
                ):

                    if pontos == 1:
                        return 3

                    if pontos == 3:
                        return 6

                    if pontos == 6:
                        return 9

                    if pontos == 9:
                        return 12

                if nao.collidepoint(
                    evento.pos
                ):

                    return pontos

        pygame.display.flip()

        clock.tick(FPS)


# ==========================================================
# COMPUTADOR PEDE TRUCO
# ==========================================================

def computador_pede_truco(
    pontos,
    carta,
    vira
):

    forca = valor_carta(
        carta,
        vira
    )

    if (
        forca >= 100
        and pontos < 12
    ):

        return True

    if (
        carta.valor in [
            "3",
            "2",
            "A"
        ]
        and pontos <= 3
    ):

        return random.choice(
            [True, False]
        )

    return False


# ==========================================================
# DESENHAR MESA
# ==========================================================

def desenhar_mesa(
    vira,
    cartas_jogador,
    carta_jogador,
    carta_computador,
    pontos_jogador,
    pontos_computador,
    pontos_rodada,
    numero_vaza
):

    TELA.fill(FUNDO)

    # Título

    desenhar_texto(
        "TRUCO PAULISTA",
        LARGURA // 2,
        35,
        FONTE_GRANDE,
        BRANCO,
        True
    )

    # Placar

    pygame.draw.rect(
        TELA,
        FUNDO_ESCURO,
        (20, 65, 270, 85),
        border_radius=12
    )

    desenhar_texto(
        f"Você: {pontos_jogador}",
        40,
        80,
        FONTE
    )

    desenhar_texto(
        f"Computador: {pontos_computador}",
        40,
        112,
        FONTE
    )

    # Valor da mão

    desenhar_texto(
        f"Valor da mão: {pontos_rodada}",
        LARGURA // 2,
        90,
        FONTE,
        DOURADO,
        True
    )

    # Vira

    desenhar_texto(
        "VIRA",
        930,
        65,
        FONTE_PEQUENA,
        BRANCO,
        True
    )

    desenhar_carta(
        vira,
        pygame.Rect(
            875,
            85,
            110,
            85
        )
    )

    # Computador

    desenhar_texto(
        "COMPUTADOR",
        LARGURA // 2,
        155,
        FONTE,
        BRANCO,
        True
    )

    # Carta do computador

    if carta_computador:

        rect = pygame.Rect(
            450,
            180,
            140,
            95
        )

        pygame.draw.rect(
            TELA,
            (90, 45, 120),
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            TELA,
            BRANCO,
            rect,
            3,
            border_radius=10
        )

        desenhar_texto(
            "?",
            rect.centerx,
            rect.centery,
            FONTE_GRANDE,
            BRANCO,
            True
        )

    # Carta do jogador jogada

    if carta_jogador:

        desenhar_carta(
            carta_jogador,
            pygame.Rect(
                600,
                180,
                140,
                95
            )
        )

    # Suas cartas

    desenhar_texto(
        "SUAS CARTAS",
        LARGURA // 2,
        335,
        FONTE,
        BRANCO,
        True
    )

    desenhar_mao(
        cartas_jogador,
        370
    )


# ==========================================================
# ESPERAR BOTÃO
# ==========================================================

def esperar_clique(botao):

    clock = pygame.time.Clock()

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if (
                evento.type
                == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):

                if botao.collidepoint(
                    evento.pos
                ):

                    return

        pygame.display.flip()

        clock.tick(FPS)


# ==========================================================
# JOGAR MÃO
# ==========================================================

def jogar_mao(
    pontos_jogador,
    pontos_computador
):

    baralho = criar_baralho()

    random.shuffle(
        baralho
    )

    jogador = []

    computador = []

    for _ in range(3):

        jogador.append(
            baralho.pop()
        )

        computador.append(
            baralho.pop()
        )

    vira = baralho.pop()

    pontos_rodada = 1

    vitorias_jogador = 0

    vitorias_computador = 0

    # ======================================================
    # 3 VAZAS
    # ======================================================

    for numero_vaza in range(1, 4):

        carta_jogador = None

        carta_computador = None

        # ==================================================
        # COMPUTADOR PODE PEDIR TRUCO
        # ==================================================

        if (
            computador
            and numero_vaza < 3
            and computador_pede_truco(
                pontos_rodada,
                computador[0],
                vira
            )
        ):

            novo_valor = tela_truco(
                pontos_rodada
            )

            if novo_valor == 0:

                return (
                    "computador",
                    pontos_rodada
                )

            pontos_rodada = novo_valor

        # ==================================================
        # JOGADOR ESCOLHE CARTA
        # ==================================================

        selecionada = -1

        clock = pygame.time.Clock()

        while carta_jogador is None:

            TELA.fill(FUNDO)

            desenhar_mesa(
                vira,
                jogador,
                None,
                None,
                pontos_jogador,
                pontos_computador,
                pontos_rodada,
                numero_vaza
            )

            largura = 145

            altura = 100

            espacamento = 25

            total = (
                len(jogador) * largura
                + max(
                    0,
                    len(jogador) - 1
                ) * espacamento
            )

            x = (
                LARGURA - total
            ) // 2

            rects = []

            for i, carta in enumerate(
                jogador
            ):

                rect = pygame.Rect(
                    x + i * (
                        largura
                        + espacamento
                    ),
                    370,
                    largura,
                    altura
                )

                desenhar_carta(
                    carta,
                    rect,
                    i == selecionada
                )

                rects.append(
                    rect
                )

            desenhar_texto(
                "Clique em uma carta para jogar",
                LARGURA // 2,
                520,
                FONTE_PEQUENA,
                CINZA,
                True
            )

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEMOTION:

                    selecionada = -1

                    for i, rect in enumerate(
                        rects
                    ):

                        if rect.collidepoint(
                            evento.pos
                        ):

                            selecionada = i

                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    for i, rect in enumerate(
                        rects
                    ):

                        if rect.collidepoint(
                            evento.pos
                        ):

                            carta_jogador = (
                                jogador.pop(i)
                            )

                            break

            pygame.display.flip()

            clock.tick(FPS)

        # ==================================================
        # COMPUTADOR ESCOLHE CARTA
        # ==================================================

        cartas_que_vencem = []

        for carta in computador:

            if (
                valor_carta(
                    carta,
                    vira
                )
                >
                valor_carta(
                    carta_jogador,
                    vira
                )
            ):

                cartas_que_vencem.append(
                    carta
                )

        if cartas_que_vencem:

            carta_computador = min(
                cartas_que_vencem,
                key=lambda c:
                valor_carta(c, vira)
            )

        else:

            carta_computador = random.choice(
                computador
            )

        computador.remove(
            carta_computador
        )

        # ==================================================
        # VERIFICAR VENCEDOR
        # ==================================================

        valor_jogador = valor_carta(
            carta_jogador,
            vira
        )

        valor_computador = valor_carta(
            carta_computador,
            vira
        )

        if valor_jogador > valor_computador:

            vitorias_jogador += 1

            resultado = (
                "Você ganhou a vaza!"
            )

        elif valor_computador > valor_jogador:

            vitorias_computador += 1

            resultado = (
                "O computador ganhou a vaza!"
            )

        else:

            resultado = "Empate!"

            if (
                vitorias_jogador
                >
                vitorias_computador
            ):

                vitorias_jogador += 1

            elif (
                vitorias_computador
                >
                vitorias_jogador
            ):

                vitorias_computador += 1

        # ==================================================
        # MOSTRAR RESULTADO
        # ==================================================

        desenhar_mesa(
            vira,
            jogador,
            carta_jogador,
            carta_computador,
            pontos_jogador,
            pontos_computador,
            pontos_rodada,
            numero_vaza
        )

        desenhar_texto(
            resultado,
            LARGURA // 2,
            550,
            FONTE,
            DOURADO,
            True
        )

        desenhar_texto(
            f"Vazas: Você {vitorias_jogador} x "
            f"{vitorias_computador} Computador",
            LARGURA // 2,
            590,
            FONTE_PEQUENA,
            BRANCO,
            True
        )

        botao = pygame.Rect(
            430,
            625,
            240,
            50
        )

        desenhar_botao(
            botao,
            "CONTINUAR"
        )

        pygame.display.flip()

        esperar_clique(
            botao
        )

        # ==================================================
        # VERIFICAR FIM DA MÃO
        # ==================================================

        if vitorias_jogador >= 2:

            return (
                "jogador",
                pontos_rodada
            )

        if vitorias_computador >= 2:

            return (
                "computador",
                pontos_rodada
            )

        # ==================================================
        # JOGADOR PODE PEDIR TRUCO
        # ==================================================

        if (
            numero_vaza < 3
            and pontos_rodada < 12
        ):

            novo_valor = (
                perguntar_truco_jogador(
                    pontos_rodada
                )
            )

            if novo_valor > pontos_rodada:

                aceitar = random.choice(
                    [
                        True,
                        True,
                        False
                    ]
                )

                if not aceitar:

                    return (
                        "jogador",
                        pontos_rodada
                    )

                pontos_rodada = novo_valor

    # ======================================================
    # RESULTADO
    # ======================================================

    if (
        vitorias_jogador
        >
        vitorias_computador
    ):

        return (
            "jogador",
            pontos_rodada
        )

    elif (
        vitorias_computador
        >
        vitorias_jogador
    ):

        return (
            "computador",
            pontos_rodada
        )

    return (
        "empate",
        pontos_rodada
    )


# ==========================================================
# RESULTADO DA MÃO
# ==========================================================

def tela_fim_mao(
    vencedor,
    pontos,
    pontos_jogador,
    pontos_computador
):

    clock = pygame.time.Clock()

    if vencedor == "jogador":

        titulo = (
            "VOCÊ GANHOU A MÃO!"
        )

    elif vencedor == "computador":

        titulo = (
            "COMPUTADOR GANHOU A MÃO!"
        )

    else:

        titulo = (
            "MÃO EMPATADA!"
        )

    while True:

        TELA.fill(FUNDO)

        desenhar_texto(
            titulo,
            LARGURA // 2,
            220,
            FONTE_GRANDE,
            BRANCO,
            True
        )

        desenhar_texto(
            f"Valor: {pontos} ponto(s)",
            LARGURA // 2,
            285,
            FONTE,
            DOURADO,
            True
        )

        desenhar_texto(
            f"Placar: Você {pontos_jogador} "
            f"x {pontos_computador} Computador",
            LARGURA // 2,
            330,
            FONTE,
            BRANCO,
            True
        )

        botao = pygame.Rect(
            400,
            410,
            300,
            60
        )

        desenhar_botao(
            botao,
            "PRÓXIMA MÃO"
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if (
                evento.type
                == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):

                if botao.collidepoint(
                    evento.pos
                ):

                    return

        pygame.display.flip()

        clock.tick(FPS)


# ==========================================================
# TELA FINAL
# ==========================================================

def tela_final(
    pontos_jogador,
    pontos_computador
):

    clock = pygame.time.Clock()

    while True:

        TELA.fill(FUNDO)

        if pontos_jogador >= 12:

            titulo = (
                "PARABÉNS! VOCÊ VENCEU!"
            )

        else:

            titulo = (
                "O COMPUTADOR VENCEU!"
            )

        desenhar_texto(
            titulo,
            LARGURA // 2,
            200,
            FONTE_GRANDE,
            BRANCO,
            True
        )

        desenhar_texto(
            f"Você: {pontos_jogador} "
            f" | Computador: {pontos_computador}",
            LARGURA // 2,
            275,
            FONTE,
            BRANCO,
            True
        )

        jogar_novamente = pygame.Rect(
            330,
            370,
            200,
            60
        )

        sair = pygame.Rect(
            570,
            370,
            200,
            60
        )

        desenhar_botao(
            jogar_novamente,
            "JOGAR NOVAMENTE"
        )

        desenhar_botao(
            sair,
            "SAIR"
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if (
                evento.type
                == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):

                if jogar_novamente.collidepoint(
                    evento.pos
                ):

                    return True

                if sair.collidepoint(
                    evento.pos
                ):

                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

        clock.tick(FPS)


# ==========================================================
# JOGO PRINCIPAL
# ==========================================================

def jogar():

    while True:

        pontos_jogador = 0

        pontos_computador = 0

        while (
            pontos_jogador < 12
            and pontos_computador < 12
        ):

            vencedor, pontos = jogar_mao(
                pontos_jogador,
                pontos_computador
            )

            if vencedor == "jogador":

                pontos_jogador += pontos

            elif vencedor == "computador":

                pontos_computador += pontos

            tela_fim_mao(
                vencedor,
                pontos,
                pontos_jogador,
                pontos_computador
            )

        jogar_novamente = tela_final(
            pontos_jogador,
            pontos_computador
        )

        if not jogar_novamente:

            break


# ==========================================================
# INICIAR
# ==========================================================

if __name__ == "__main__":

    jogar()