import pyautogui
import time
from PIL import Image

# Importando nossas configurações e utilitários
from src.config import *
from src.utils import *

def encontrar_proximo_alvo(imagem_gabarito_redimensionada, last_x, last_y):

    screenshot_jogo = Image.open(CAMINHO_SCREENSHOT_TEMP).convert('RGBA')

    # Correção usando a divisão de piso //
    screenshot_jogo_redimensionada = screenshot_jogo.resize(
        (int(imagem_gabarito_redimensionada.width), int(imagem_gabarito_redimensionada.height)), 
        Image.Resampling.NEAREST
    )

    screenshot_jogo_redimensionada.save(CAMINHO_SCREENSHOT_TEMP_REDIMENSIONADA)

    w, h = screenshot_jogo_redimensionada.size

    for i in range(w * h):
        
        # Calculate the index of the pixel to check
        pixel_index = ((last_y * w + last_x) + 1 + i) % (w * h)
        x_rel = pixel_index % w
        y_rel = pixel_index // w

        cor_gabarito_rgba = imagem_gabarito_redimensionada.getpixel((x_rel, y_rel))

        if cor_gabarito_rgba[3] < 255:
            continue

        cor_gabarito_rgb = cor_gabarito_rgba[:3]
        
        cor_ideal_na_paleta = encontrar_cor_mais_proxima(cor_gabarito_rgb, PALETA_DE_CORES)
        cor_atual_jogo_rgb = screenshot_jogo_redimensionada.getpixel((x_rel, y_rel))[:3]

        # 3. Compara a cor da tela com a cor ideal DA PALETA, não do gabarito.
        if not cores_sao_proximas(cor_ideal_na_paleta, cor_atual_jogo_rgb, TOLERANCIA_COR):

            print(f"🎯 Alvo encontrado em ({x_rel}, {y_rel}). Cor Gabarito: {cor_gabarito_rgb}, Cor na Tela: {cor_atual_jogo_rgb}")

            x_cor = mecanismo_de_correção_de_pixels(screenshot_jogo.width, x_rel, w) // 1
            y_cor = mecanismo_de_correção_de_pixels(screenshot_jogo.height, y_rel, h) // 1

            x_OG = (x_rel * ESCALA_DE_PIXELS + ESCALA_DE_PIXELS / 2) // 2 + x_cor
            y_OG = (y_rel * ESCALA_DE_PIXELS + ESCALA_DE_PIXELS / 2) // 2 + y_cor

            print(f"Coordenada corrigida: ({x_cor}, {y_cor})")
            print(f"Coordenada com correção: ({x_OG}, {y_OG})")
            print(f"Coordenada redimensionada: ({x_rel}, {y_rel})")

            return [{'coord_arte': (x_OG, y_OG), 'cor_alvo': cor_gabarito_rgb}, x_rel, y_rel]

    return None, last_x, last_y

def pintar_pixel(coord_arte, cor_alvo, cor_anterior):
    """
    Encontra a cor na paleta e usa cliques humanizados para pintar o pixel no mapa,
    COM A LÓGICA DE COORDENADAS CORRIGIDA para telas Retina e gabaritos 2x.
    """
    cor_na_paleta = encontrar_cor_mais_proxima(cor_alvo, PALETA_DE_CORES)
    if not cor_na_paleta or cor_na_paleta not in PALETA_DE_CORES:
        return

    pos_cor_na_tela = PALETA_DE_CORES[cor_na_paleta]

    # ================== A CORREÇÃO FINAL ESTÁ AQUI ==================
    # Para garantir que o clique aconteça no CENTRO do pixel do jogo e não na borda,
    # adicionamos um pequeno deslocamento de meio "ponto".

    pos_mapa_na_tela = (
        PONTO_DE_ORIGEM_MAPA[0] + coord_arte[0],
        PONTO_DE_ORIGEM_MAPA[1] + coord_arte[1]
    )
    # =================================================================

    print(f"Corrigindo pixel em {pos_mapa_na_tela} para a cor {cor_alvo}...")
    try:
        if (cor_anterior != cor_na_paleta):
            print(f"A melhor cor para o trabalho é {cor_na_paleta}")
            pyautogui.click(pos_cor_na_tela[0], pos_cor_na_tela[1])
            time.sleep(0.4 * SLEEP_COEFICIENT)

        pyautogui.click(pos_mapa_na_tela[0], pos_mapa_na_tela[1])
        time.sleep(0.3 * SLEEP_COEFICIENT)

        return cor_na_paleta

    except Exception as e:
        print(f"❌ Ocorreu um erro ao tentar pintar: {e}")
