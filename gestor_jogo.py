import random
import pygame
import math
from config import *
from ui import fonte_menu, fonte_titulo
from entidades import Jogador, Inimigo, Boss, Tiro

class GestorJogo:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.jogador = Jogador(LARGURA // 2 - 16, ALTURA // 2)
        self.tiros_jogador = []
        self.tiros_inimigos = []
        self.invasores = []
        self.boss = None
        self.em_boss = False
        self.onda_atual = 1
        self.pontuacao = 0
        self.jogo_over = False
        self.jogo_venceu = False
        self.total_inimigos_onda = 0
        self.iniciar_onda()

    def iniciar_onda(self):
        self.invasores.clear()
        self.tiros_jogador.clear()
        self.tiros_inimigos.clear()

        if self.onda_atual % 3 == 0:
            self.em_boss = True
            self.boss = Boss(LARGURA // 2 - 45, 40)
        else:
            self.em_boss = False
            self.boss = None
            self.total_inimigos_onda = 10 + (self.onda_atual * 5)

    def gerar_inimigo_aleatorio(self):
        x = random.randint(160, LARGURA - 190)
        y = random.randint(-60, -20)
        vel = random.uniform(1.8, 2.5) + (self.onda_atual * 0.1)
        return Inimigo(x, y, velocidade=vel)

    def atualizar(self):
        if self.jogo_over or self.jogo_venceu:
            return

        teclas = pygame.key.get_pressed()
        self.jogador.atualizar(teclas)

        tiro_dx, tiro_dy = 0, 0
        if teclas[pygame.K_LEFT]:
            tiro_dx -= 1
        if teclas[pygame.K_RIGHT]:
            tiro_dx += 1
        if teclas[pygame.K_UP]:
            tiro_dy -= 1
        if teclas[pygame.K_DOWN]:
            tiro_dy += 1

        if (tiro_dx != 0 or tiro_dy != 0) and self.jogador.contador_tiro == 0:
            dist = math.hypot(tiro_dx, tiro_dy)
            dx_norm = tiro_dx / dist
            dy_norm = tiro_dy / dist

            cx, cy = self.jogador.rect.centerx, self.jogador.rect.centery
            
            if self.jogador.tiro_duplo:
                perp_x, perp_y = -dy_norm * 8, dx_norm * 8
                self.tiros_jogador.append(Tiro(cx + perp_x, cy + perp_y, dx_norm, dy_norm, velocidade=10, cor=COR_TIRO_JOGADOR))
                self.tiros_jogador.append(Tiro(cx - perp_x, cy - perp_y, dx_norm, dy_norm, velocidade=10, cor=COR_TIRO_JOGADOR))
            else:
                self.tiros_jogador.append(Tiro(cx, cy, dx_norm, dy_norm, velocidade=10, cor=COR_TIRO_JOGADOR))
                
            self.jogador.contador_tiro = self.jogador.cooldown_tiro

        for t in self.tiros_jogador[:]:
            t.atualizar()
            if t.rect.right < 0 or t.rect.left > LARGURA or t.rect.bottom < 0 or t.rect.top > ALTURA:
                self.tiros_jogador.remove(t)

        if not self.em_boss:
            if self.total_inimigos_onda > 0 and random.random() < 0.04:
                self.invasores.append(self.gerar_inimigo_aleatorio())
                self.total_inimigos_onda -= 1

            for inv in self.invasores[:]:
                dir_x, dir_y = inv.perseguir_jogador(self.jogador.rect)

                if inv.rect.colliderect(self.jogador.rect):
                    self.jogador.vidas -= 1
                    self.invasores.remove(inv)
                    if self.jogador.vidas <= 0:
                        self.jogo_over = True

                if random.random() < 0.003:
                    self.tiros_inimigos.append(
                        Tiro(inv.rect.centerx, inv.rect.centery, dir_x, dir_y, velocidade=5, cor=COR_PERIGO)
                    )

        elif self.em_boss and self.boss:
            dir_x, dir_y = self.boss.perseguir_jogador(self.jogador.rect)

            if self.boss.rect.colliderect(self.jogador.rect):
                self.jogador.vidas -= 1
                if self.jogador.vidas <= 0:
                    self.jogo_over = True

            if random.random() < 0.04:
                self.tiros_inimigos.append(
                    Tiro(self.boss.rect.centerx, self.boss.rect.centery, dir_x, dir_y, velocidade=6, cor=COR_PERIGO)
                )

        for t in self.tiros_inimigos[:]:
            t.atualizar()
            if t.rect.right < 0 or t.rect.left > LARGURA or t.rect.bottom < 0 or t.rect.top > ALTURA:
                self.tiros_inimigos.remove(t)
            elif t.rect.colliderect(self.jogador.rect):
                self.tiros_inimigos.remove(t)
                self.jogador.vidas -= 1
                if self.jogador.vidas <= 0:
                    self.jogo_over = True

        for t in self.tiros_jogador[:]:
            if self.em_boss and self.boss and t.rect.colliderect(self.boss.rect):
                self.tiros_jogador.remove(t)
                self.boss.vida -= self.jogador.dano
                if self.boss.vida <= 0:
                    self.pontuacao += 500
                    self.boss = None
                    self.onda_atual += 1
                    self.iniciar_onda()
                break
            else:
                for inv in self.invasores[:]:
                    if t.rect.colliderect(inv.rect):
                        self.tiros_jogador.remove(t)
                        self.invasores.remove(inv)
                        self.pontuacao += 15
                        break

        if not self.em_boss and self.total_inimigos_onda <= 0 and len(self.invasores) == 0:
            self.onda_atual += 1
            self.iniciar_onda()

    def desenhar(self, superficie):
        txt_pontos = fonte_menu.render(f"PONTOS: {self.pontuacao}", True, BRANCO_FOSCO)
        txt_onda = fonte_menu.render(f"ONDA: {self.onda_atual}", True, AZUL_HOVER)
        txt_vidas = fonte_menu.render(f"VIDAS: {self.jogador.vidas}", True, COR_HUD)

        superficie.blit(txt_pontos, (170, 40))
        superficie.blit(txt_onda, (LARGURA // 2 - txt_onda.get_width() // 2, 40))
        superficie.blit(txt_vidas, (LARGURA - 170 - txt_vidas.get_width(), 40))

        if not self.jogo_over:
            self.jogador.desenhar(superficie)

        for inv in self.invasores:
            pygame.draw.rect(superficie, COR_INVASOR, inv.rect, border_radius=4)
            pygame.draw.rect(superficie, COR_INVASOR_BORDA, inv.rect, 1, border_radius=4)

        if self.em_boss and self.boss:
            self.boss.desenhar(superficie)

        for t in self.tiros_jogador:
            t.desenhar(superficie)

        for t in self.tiros_inimigos:
            t.desenhar(superficie)

        if self.jogo_over:
            txt_fim = fonte_titulo.render("GAME OVER", True, COR_PERIGO)
            superficie.blit(txt_fim, txt_fim.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40)))