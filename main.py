import pygame
import sys
from config import *
from ui import Botao, fonte_titulo, fonte_subtitulo, fonte_menu, fonte_comum
from gestor_jogo import GestorJogo

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cidade das Cinzas")
relogio = pygame.time.Clock()

estado_atual = TELA_INICIAL
tempo_texto = 0
mostrar_prompt = True

volume_musica = 80
volume_sfx = 90
resolucao_selecionada = 0
opcoes_resolucao = ["1920x1080 (FHD)", "1280x720 (HD)", "Janela"]

gestor_jogo = GestorJogo()

def acao_jogar():
    global estado_atual
    estado_atual = TELA_JOGAR
    gestor_jogo.reiniciar()

def acao_config():
    global estado_atual
    estado_atual = TELA_CONFIG

def acao_creditos():
    global estado_atual
    estado_atual = TELA_CREDITOS

def acao_voltar():
    global estado_atual
    estado_atual = TELA_MENU

botoes_menu = [
    Botao(LARGURA // 2, 280, 280, 50, "JOGAR", acao_jogar),
    Botao(LARGURA // 2, 350, 280, 50, "CONFIGURAÇÕES", acao_config),
    Botao(LARGURA // 2, 420, 280, 50, "CRÉDITOS", acao_creditos),
]

botao_voltar_config = Botao(LARGURA // 2, 480, 280, 50, "VOLTAR", acao_voltar)
botao_voltar_creditos = Botao(LARGURA // 2, 480, 280, 50, "VOLTAR", acao_voltar)
botao_voltar_jogo = Botao(LARGURA // 2, 560, 280, 35, "SAIR PARA O MENU", acao_voltar)

# Loop Principal
executando = True
while executando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            executando = False

        if estado_atual == TELA_INICIAL:
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                estado_atual = TELA_MENU

        elif estado_atual == TELA_MENU:
            for btn in botoes_menu:
                btn.checar_clique(evento)

        elif estado_atual == TELA_CONFIG:
            botao_voltar_config.checar_clique(evento)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                if 220 <= mouse_y <= 240 and 420 <= mouse_x <= 570:
                    volume_musica = int((mouse_x - 420) / 150 * 100)
                elif 280 <= mouse_y <= 300 and 420 <= mouse_x <= 570:
                    volume_sfx = int((mouse_x - 420) / 150 * 100)
                elif 340 <= mouse_y <= 370 and 420 <= mouse_x <= 570:
                    resolucao_selecionada = (resolucao_selecionada + 1) % len(opcoes_resolucao)

        elif estado_atual == TELA_CREDITOS:
            botao_voltar_creditos.checar_clique(evento)

        elif estado_atual == TELA_JOGAR:
            botao_voltar_jogo.checar_clique(evento)

    tela.fill(COR_BG)

    if estado_atual == TELA_INICIAL:
        txt_titulo = fonte_titulo.render("CIDADE DAS CINZAS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, ALTURA // 3 + 20)))

        tempo_texto += 1
        if tempo_texto % 35 == 0:
            mostrar_prompt = not mostrar_prompt

        if mostrar_prompt:
            txt_prompt = fonte_subtitulo.render("CLIQUE PARA INICIAR", True, AZUL_ESCURO)
            tela.blit(txt_prompt, txt_prompt.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50)))

    elif estado_atual == TELA_MENU:
        txt_titulo = fonte_titulo.render("CIDADE DAS CINZAS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, 150)))
        for btn in botoes_menu:
            btn.desenhar(tela)

    elif estado_atual == TELA_CONFIG:
        painel_rect = pygame.Rect(150, 80, 500, 440)
        pygame.draw.rect(tela, COR_PAINEL, painel_rect, border_radius=8)
        pygame.draw.rect(tela, COR_BORDA_DARK, painel_rect, 1, border_radius=8)

        txt_titulo = fonte_titulo.render("CONFIGS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, 140)))

        tela.blit(fonte_menu.render("Volume Música:", True, BRANCO_FOSCO), (180, 220))
        pygame.draw.rect(tela, CINZA_BARRA, (420, 230, 150, 6), border_radius=3)
        pygame.draw.rect(tela, AZUL_ESCURO, (420, 230, int(volume_musica * 1.5), 6), border_radius=3)

        tela.blit(fonte_menu.render("Volume Geral:", True, BRANCO_FOSCO), (180, 280))
        pygame.draw.rect(tela, CINZA_BARRA, (420, 290, 150, 6), border_radius=3)
        pygame.draw.rect(tela, AZUL_ESCURO, (420, 290, int(volume_sfx * 1.5), 6), border_radius=3)

        tela.blit(fonte_menu.render("Resolução:", True, BRANCO_FOSCO), (180, 340))
        tela.blit(fonte_comum.render(opcoes_resolucao[resolucao_selecionada], True, CINZA_TEXTO), (420, 342))

        botao_voltar_config.desenhar(tela)

    elif estado_atual == TELA_CREDITOS:
        painel_rect = pygame.Rect(150, 80, 500, 440)
        pygame.draw.rect(tela, COR_PAINEL, painel_rect, border_radius=8)
        pygame.draw.rect(tela, COR_BORDA_DARK, painel_rect, 1, border_radius=8)

        txt_titulo = fonte_titulo.render("CRÉDITOS", True, BRANCO_FOSCO)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA // 2, 140)))

        txt_desenv = fonte_menu.render("DESENVOLVIDO POR:", True, CINZA_TEXTO)
        tela.blit(txt_desenv, txt_desenv.get_rect(center=(LARGURA // 2, 220)))

        txt_nomes = fonte_menu.render("Christophe, João Paulo e Alessandro", True, BRANCO_FOSCO)
        tela.blit(txt_nomes, txt_nomes.get_rect(center=(LARGURA // 2, 260)))

        botao_voltar_creditos.desenhar(tela)

    elif estado_atual == TELA_JOGAR:
        painel_rect = pygame.Rect(150, 20, 500, 560)
        pygame.draw.rect(tela, COR_PAINEL, painel_rect, border_radius=8)
        pygame.draw.rect(tela, AZUL_ESCURO, painel_rect, 1, border_radius=8)

        gestor_jogo.atualizar()
        gestor_jogo.desenhar(tela)
        botao_voltar_jogo.desenhar(tela)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()