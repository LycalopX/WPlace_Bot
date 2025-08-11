
import math
from config import *

# ==============================================================================
# =========================== FUNÇÕES AUXILIARES ===============================
# ==============================================================================

def cores_sao_proximas(cor1, cor2, tolerancia):
    """Verifica se duas cores RGB são suficientemente próximas com base na tolerância."""
    if cor1 is None or cor2 is None: return False
    distancia = math.sqrt(sum([(a - b) ** 2 for a, b in zip(cor1, cor2)]))
    return distancia < tolerancia

def encontrar_cor_mais_proxima(cor_alvo, paleta):
    """Encontra a cor mais próxima disponível na paleta do jogo."""
    return min(paleta.keys(), key=lambda cor: math.sqrt(sum([(a - b) ** 2 for a, b in zip(cor_alvo, cor)])))

def mecanismo_de_correção_de_pixels(dim_original, dim_pixel, dim_pixel_completa):
    """Calcula correção de pixels da imagem original para a imagem redimensionada."""

    porcentagem_percorrida = dim_pixel / dim_pixel_completa
    print(f"Porcentagem percorrida: {porcentagem_percorrida:.2f}")
    cor = (dim_original - ESCALA_DE_PIXELS * dim_pixel_completa) * porcentagem_percorrida
    print(f"Cor corrigida: {cor:.2f}")

    return cor
