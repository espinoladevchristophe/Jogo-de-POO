import pygame
from config import AZUL_HOVER, COR_BORDA_DARK, COR_PAINEL, BRANCO_FOSCO

pygame.font.init()
try:
    fonte_titulo = pygame.font.SysFont("impact", 74)
    fonte_subtitulo = pygame.font.SysFont("arial", 20, bold=True)
    fonte_menu = pygame.font.SysFont("arial", 22, bold=True)
    fonte_comum = pygame.font.SysFont("arial", 18)
except:
    fonte_titulo = pygame.font.Font(None, 80)
    fonte_subtitulo = pygame.font.Font(None, 26)
    fonte_menu = pygame.font.Font(None, 30)
    fonte_comum = pygame.font.Font(None, 22)

class Botao:
    def __init__(self, x, y, largura, altura, texto, acao):
        self.rect = pygame.Rect(x - largura // 2, y, largura, altura)
        self.texto = texto
        self.acao = acao
        self.hovered = False

    def desenhar(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            cor_borda = AZUL_HOVER
            cor_fundo = (25, 35, 50)
            deslocamento = 2
        else:
            self.hovered = False
            cor_borda = COR_BORDA_DARK
            cor_fundo = COR_PAINEL
            deslocamento = 0

        pygame.draw.rect(superficie, cor_fundo, self.rect.move(0, deslocamento), border_radius=4)
        pygame.draw.rect(superficie, cor_borda, self.rect.move(0, deslocamento), 1, border_radius=4)

        cor_txt = BRANCO_FOSCO if not self.hovered else AZUL_HOVER
        texto_surf = fonte_menu.render(self.texto, True, cor_txt)
        texto_rect = texto_surf.get_rect(center=self.rect.move(0, deslocamento).center)
        superficie.blit(texto_surf, texto_rect)

    def checar_clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.acao()