import pyautogui
import time
from PIL import Image
import subprocess

# Importando nossas configurações e utilitários
from config import *
from utils import *

# Lógica do bot

def encontrar_proximo_alvo(imagem_gabarito, imagem_gabarito_redimensionada, origem_mapa):
    
    x, y = origem_mapa
    w, h = imagem_gabarito.width // ESCALA_TELA, imagem_gabarito.height // ESCALA_TELA
    caminho_temp = CAMINHO_SCREENSHOT_TEMP

    try:
        print(f"Capturando área de {w}x{h} pontos começando em ({x}, {y})...")
        subprocess.run(['screencapture', '-x', '-R', f'{x},{y},{w},{h}', caminho_temp], check=True)

    except Exception as e:
        print(f"❌ Erro ao usar 'screencapture': {e}")
        return None
    
    w = w // ESCALA_DE_PIXELS * ESCALA_TELA
    h = h // ESCALA_DE_PIXELS * ESCALA_TELA

    screenshot_jogo = Image.open(caminho_temp).convert('RGBA')
    screenshot_jogo_redimensionada = screenshot_jogo.resize((screenshot_jogo.width // ESCALA_DE_PIXELS, screenshot_jogo.height // ESCALA_DE_PIXELS), Image.Resampling.NEAREST)
    screenshot_jogo_redimensionada.save(CAMINHO_SCREENSHOT_TEMP_REDIMENSIONADA)

    for y_rel in range(h):
        for x_rel in range(w):

            cor_gabarito_rgba = imagem_gabarito_redimensionada.getpixel((x_rel, y_rel))

            if cor_gabarito_rgba[3] < 255:
                continue
            
            cor_gabarito_rgb = cor_gabarito_rgba[:3]
            
            cor_ideal_na_paleta = encontrar_cor_mais_proxima(cor_gabarito_rgb, PALETA_DE_CORES)
            cor_atual_jogo_rgb = screenshot_jogo_redimensionada.getpixel((x_rel, y_rel))[:3]

            # 3. Compara a cor da tela com a cor ideal DA PALETA, não do gabarito.
            if not cores_sao_proximas(cor_ideal_na_paleta, cor_atual_jogo_rgb, TOLERANCIA_COR):
                print(f"🎯 Alvo encontrado em ({x_rel}, {y_rel}). Cor Gabarito: {cor_gabarito_rgb}, Cor na Tela: {cor_atual_jogo_rgb}")

                x_cor = mecanismo_de_correção_de_pixels(screenshot_jogo.width, x_rel, w)
                y_cor = mecanismo_de_correção_de_pixels(screenshot_jogo.height, y_rel, h)
                x_cor = x_cor - (x_cor % 1)
                y_cor = y_cor - (y_cor % 1)

                x_OG = (x_rel * ESCALA_DE_PIXELS + ESCALA_DE_PIXELS / 2) / 2 + x_cor
                y_OG = (y_rel * ESCALA_DE_PIXELS + ESCALA_DE_PIXELS / 2) / 2 + y_cor

                print(f"Coordenada corrigida: ({x_OG}, {y_OG})")
                print(f"Coordenada redimensionada: ({x_rel}, {y_rel})")

                return {'coord_arte': (x_OG, y_OG), 'cor_alvo': cor_gabarito_rgb}

    return None

def pintar_pixel(coord_arte, cor_alvo):
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
        # A sequência de cliques humanizados continua a mesma.
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])
        time.sleep(0.2)

        pyautogui.click(pos_cor_na_tela[0], pos_cor_na_tela[1])
        time.sleep(0.2)

        pyautogui.click(pos_mapa_na_tela[0], pos_mapa_na_tela[1])
        time.sleep(0.2)

        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])
    except Exception as e:
        print(f"❌ Ocorreu um erro ao tentar pintar: {e}")

if __name__ == "__main__":
    
    print("Carregando imagem gabarito...")
    try:
        imagem_gabarito = Image.open(CAMINHO_IMAGEM_A_PINTAR).convert('RGBA')
        imagem_gabarito_redimensionada = Image.open(CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA).convert('RGBA')

    except FileNotFoundError:
        print(f"❌ ERRO FATAL: Imagem gabarito '{CAMINHO_IMAGEM_A_PINTAR}'/'{CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA}' não encontrada.")
        exit()
        
    print(f"Gabarito '{CAMINHO_IMAGEM_A_PINTAR}' carregado ({imagem_gabarito.width}x{imagem_gabarito.height}).")
    print(">>> INICIANDO BOT CORRETOR EM 5 SEGUNDOS <<<")
    time.sleep(5)
    
    while True:        

        alvo = encontrar_proximo_alvo(imagem_gabarito, imagem_gabarito_redimensionada, PONTO_DE_ORIGEM_MAPA)
        if alvo is None:
            print("\n✅🎉====== DESENHO CONCLUÍDO E VERIFICADO! ======🎉✅")
            print("Aguardando 180 segundos antes de verificar novamente...")
            time.sleep(180)
            continue
        
        pintar_pixel(alvo['coord_arte'], alvo['cor_alvo'])
        
        print(f"Aguardando cooldown de {COOLDOWN_ENTRE_ACOES} segundos...")
        time.sleep(COOLDOWN_ENTRE_ACOES)