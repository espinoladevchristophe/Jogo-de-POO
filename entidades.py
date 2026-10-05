import pygame
import math
from config import *

class Tiro:
    def __init__(self, x, y, dx, dy, velocidade=10, cor=COR_TIRO_JOGADOR):
        self.rect = pygame.Rect(x, y, 6, 6)
        self.dx = dx
        self.dy = dy
        self.velocidade = velocidade
        self.cor = cor

    def atualizar(self):
        self.rect.x += int(self.dx * self.velocidade)
        self.rect.y += int(self.dy * self.velocidade)

    def desenhar(self, superficie):
        pygame.draw.circle(superficie, self.cor, self.rect.center, 3)


class Jogador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocidade = 5
        self.vidas = 3
        self.cooldown_tiro = 12
        self.contador_tiro = 0
        
        # Upgrades
        self.dano = 1
        self.tiro_duplo = False

    def atualizar(self, teclas):
        dx, dy = 0, 0
        
        if teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_s]:
            dy += 1

        if dx != 0 or dy != 0:
            dist = math.hypot(dx, dy)
            dx_norm = dx / dist
            dy_norm = dy / dist
            self.rect.x += int(dx_norm * self.velocidade)
            self.rect.y += int(dy_norm * self.velocidade)

        self.rect.left = max(160, self.rect.left)
        self.rect.right = min(LARGURA - 160, self.rect.right)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(ALTURA - 30, self.rect.bottom)

        if self.contador_tiro > 0:
            self.contador_tiro -= 1

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, AZUL_ESCURO, self.rect, border_radius=4)
        pygame.draw.polygon(
            superficie,
            AZUL_HOVER,
            [
                (self.rect.centerx, self.rect.top - 8),
                (self.rect.left + 4, self.rect.bottom),
                (self.rect.right - 4, self.rect.bottom),
            ],
        )


class Inimigo:
    def __init__(self, x, y, velocidade=2):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.velocidade = velocidade
        self.vida = 1

    def perseguir_jogador(self, jogador_rect):
        dx = jogador_rect.centerx - self.rect.centerx
        dy = jogador_rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia != 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += int(dx * self.velocidade)
            self.rect.y += int(dy * self.velocidade)
            return dx, dy
        return 0, 1


class Boss:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 90)
        self.vida_maxima = 60
        self.vida = 60
        self.velocidade = 1.8

    def perseguir_jogador(self, jogador_rect):
        dx = jogador_rect.centerx - self.rect.centerx
        dy = jogador_rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia != 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += int(dx * self.velocidade)
            self.rect.y += int(dy * self.velocidade)
            return dx, dy
        return 0, 1

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, COR_PERIGO, self.rect, border_radius=8)
        largura_barra = int(90 * (self.vida / self.vida_maxima))
        if largura_barra > 0:
            pygame.draw.rect(superficie, (40, 40, 40), (self.rect.x, self.rect.top - 14, 90, 6))
            pygame.draw.rect(superficie, COR_PERIGO, (self.rect.x, self.rect.top - 14, largura_barra, 6))