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

import subprocess


if __name__ == "__main__":
    
    print("Carregando imagem gabarito...")
    try:
        imagem_gabarito = Image.open(CAMINHO_IMAGEM_A_PINTAR).convert('RGBA')
        imagem_gabarito_redimensionada = Image.open(CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA).convert('RGBA')

    except FileNotFoundError:
        print(f"❌ ERRO FATAL: Imagem gabarito '{CAMINHO_IMAGEM_A_PINTAR}'/'{CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA}' não encontrada.")
        exit()
        
    print(f"Gabarito '{CAMINHO_IMAGEM_A_PINTAR}' carregado ({imagem_gabarito.width}x{imagem_gabarito.height}).")
    print(">>> INICIANDO BOT CORRETOR EM 10 SEGUNDOS <<<")
    time.sleep(10)

    i = 0
    # quantas abas é para mudar
    j = 0
    cor_anterior = None

    while True:

        if (SWITCH_TABS == 1):
            execute_tabs_cycle(j)


        x, y = PONTO_DE_ORIGEM_MAPA
        w, h = imagem_gabarito.width // ESCALA_TELA, imagem_gabarito.height // ESCALA_TELA
        caminho_temp = CAMINHO_SCREENSHOT_TEMP

        time.sleep(2)

        try:
            print(f"Capturando área de {w}x{h} pontos começando em ({x}, {y})...")
            subprocess.run(['screencapture', '-x', '-R', f'{x},{y},{w},{h}', caminho_temp], check=True)

        except Exception as e:
            print(f"❌ Erro ao usar 'screencapture': {e}")

        # A sequência de cliques humanizados continua a mesma.
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])
        time.sleep(2)
        # para preencher o captcha
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])

        for i in range (NUMERO_DE_PIXELS_POR_VEZ):
            alvo = encontrar_proximo_alvo(imagem_gabarito, imagem_gabarito_redimensionada, PONTO_DE_ORIGEM_MAPA, i)

            if alvo is None:
                print("\n✅🎉====== DESENHO CONCLUÍDO E VERIFICADO! ======🎉✅")
                print("Aguardando 180 segundos antes de verificar novamente...")

                time.sleep(2)
                pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])
                time.sleep(180)
                continue

            cor_anterior = pintar_pixel(alvo['coord_arte'], alvo['cor_alvo'], cor_anterior)
            i += 1

        time.sleep(1)
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])

        print(f"Aguardando cooldown de {COOLDOWN_ENTRE_ACOES} segundos...")
        time.sleep(COOLDOWN_ENTRE_ACOES)

        j += 1