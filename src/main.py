import time

# Importando nossas configurações e utilitários
from config import *
from utils import *
from logic import *

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