import sys
import os

# Add the project's root directory (WPlace) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

# Importando nossas configurações e utilitários
from src.config import *
from src.utils import *
from src.logic import *
import pyautogui

if __name__ == "__main__":
    playWinSound()

    print("Carregando imagem gabarito...")
    try:
        imagem_gabarito = Image.open(CAMINHO_IMAGEM_A_PINTAR).convert('RGBA')
        imagem_gabarito_redimensionada = Image.open(CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA).convert('RGBA')

    except FileNotFoundError:
        print(f"❌ ERRO FATAL: Imagem gabarito '{CAMINHO_IMAGEM_A_PINTAR}'/'{CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA}' não encontrada.")
        exit()
        
    print(f"Gabarito '{CAMINHO_IMAGEM_A_PINTAR}' carregado ({imagem_gabarito.width}x{imagem_gabarito.height}).\n")
    print(">>> INICIANDO BOT CORRETOR EM 10 SEGUNDOS <<<")
    time.sleep(10)

    n = 0
    cycle = 0
    cor_anterior = None
    x_rel, y_rel = 0, 0

    x, y = PONTO_DE_ORIGEM_MAPA
    w, h = imagem_gabarito.width, imagem_gabarito.height

    while True:

        if (SWITCH_TABS == 1):
            execute_tabs_cycle(cycle)

        # Chama a nova função única que faz todo o trabalho
        NUMERO_DE_PIXELS_POR_VEZ = find_and_read_pixel_count()

        try:
            time.sleep(1)
            print(f"Capturando tela inteira para recortar a área de {w}x{h} pontos em ({x}, {y})...")

            # 1. Captura a tela inteira
            screenshot_tela_inteira = pyautogui.screenshot()

            # 2. Calcula a área de recorte com a sua fórmula corrigida
            left = x * ESCALA_TELA
            top = y * ESCALA_TELA
            right = left + w
            bottom = top + h
            area_de_recorte = (left, top, right, bottom)

            # 3. Recorta a imagem. O resultado terá as dimensões (w, h)
            screenshot_jogo = screenshot_tela_inteira.crop(area_de_recorte)
            
            # (Opcional) Salvar a captura para depuração
            screenshot_jogo.save(CAMINHO_SCREENSHOT_TEMP)

        except Exception as e:
            print(f"❌ Erro ao capturar a tela: {e}")
            # Pula para a próxima iteração em caso de erro
            time.sleep(COOLDOWN_ENTRE_ACOES)
            continue

        
        # Correção usando a divisão de piso //
        screenshot_jogo_redimensionada = screenshot_jogo.resize(
            (int(imagem_gabarito_redimensionada.width), int(imagem_gabarito_redimensionada.height)), 
            Image.Resampling.NEAREST
        )

        screenshot_jogo_redimensionada.save(CAMINHO_SCREENSHOT_TEMP_REDIMENSIONADA)

        # Abre a paleta
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])
        time.sleep(1)

        # Para preencher o captcha (se tiver)
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])

        for n in range (NUMERO_DE_PIXELS_POR_VEZ):
            # The function now correctly returns a 3-element tuple, even on failure
            alvo, x_rel, y_rel = encontrar_proximo_alvo(screenshot_jogo, imagem_gabarito_redimensionada, screenshot_jogo_redimensionada, x_rel, y_rel)

            if alvo is None:
                print("\n✅🎉====== DESENHO CONCLUÍDO E VERIFICADO! ======🎉✅")
                print("Aguardando 180 segundos antes de verificar novamente...")

                time.sleep(2)
                # Termina o desenho
                pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])

                # Espera até o próximo ciclo de verificação
                playWinSound()
                time.sleep(180)
                
                # Break out of this for-loop and start the main while-loop again
                break 

            cor_anterior = pintar_pixel(alvo['coord_arte'], alvo['cor_alvo'], cor_anterior)

        # Termina o desenho
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])

        print(f"Aguardando cooldown de {COOLDOWN_ENTRE_ACOES} segundos...")
        time.sleep(COOLDOWN_ENTRE_ACOES)

        cycle += 1
        x_rel, y_rel = 0, 0
        cor_anterior = None
