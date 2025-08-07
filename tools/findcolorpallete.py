from PIL import Image
from collections import OrderedDict

# ==================== CONFIGURAÇÃO ====================
# 1. O caminho para o seu arquivo de screenshot (o de 2880x1800).
CAMINHO_DA_IMAGEM = 'a.png'

# 2. Fator de escala da sua tela Retina. Para 2880x1800 -> 1440x900, o fator é 2.
FATOR_ESCALA_RETINA = 2

# 3. A SUA LISTA DE CORES LIMPA.
CORES_PARA_ENCONTRAR = [
    (0, 0, 0), (254, 254, 255), (100, 113, 134), (58, 127, 111),
    (60, 60, 60), (210, 210, 210), (218, 56, 50), (239, 134, 64),
    (235, 173, 61), (244, 222, 93), (85, 182, 112), (165, 252, 117),
    (80, 171, 165), (140, 244, 241), (86, 145, 222), (158, 176, 245),
    (110, 25, 147), (157, 64, 179), (214, 162, 243), (217, 57, 127),
    (229, 146, 169), (145, 86, 76), (99, 71, 55), (142, 106, 53),
    (238, 181, 128), (120, 120, 120), (87, 13, 26), (212, 101, 49),
    (254, 250, 195), (107, 227, 134), (104, 222, 191), (50, 79, 153),
    (103, 81, 237), (186, 38, 120), (254, 255, 255), (110, 117, 139),
    (170, 170, 170), (151, 35, 37), (234, 135, 119), (152, 133, 63),
    (193, 174, 74), (229, 213, 113), (103, 147, 83), (146, 195, 124),
    (55, 119, 155), (200, 248, 242), (142, 197, 250), (73, 50, 177),
    (73, 66, 128), (120, 113, 190), (240, 185, 167), (119, 100, 84),
    (152, 133, 110), (209, 182, 152), (246, 199, 170), (107, 100, 68),
    (204, 197, 162), (52, 57, 64), (81, 106, 63), (180, 174, 236),
    (198, 132, 123), (211, 166, 109), (198, 132, 90),
]
# ======================================================

def encontrar_posicoes_escaladas(caminho_imagem, cores_a_procurar, fator_escala):
    """
    Abre uma imagem e encontra a primeira ocorrência de cada cor,
    já aplicando o fator de escala de tela Retina.
    """
    try:
        img = Image.open(caminho_imagem).convert('RGB')
        largura, altura = img.size
        coordenadas_encontradas = OrderedDict()
        cores_restantes = set(cores_a_procurar)

        print(f"🔎 Procurando {len(cores_a_procurar)} cores na imagem '{caminho_imagem}'...")
        print(f"   Aplicando fator de escala de {fator_escala}x.")

        for y in range(altura):
            for x in range(largura):
                cor_pixel = img.getpixel((x, y))
                if cor_pixel in cores_restantes:
                    # Aplica o fator de escala aqui usando divisão inteira (//)
                    coord_escalada = (x // fator_escala, y // fator_escala)
                    
                    coordenadas_encontradas.setdefault(cor_pixel, coord_escalada)
                    cores_restantes.discard(cor_pixel)
                    
                    print(f"  ✔️ Encontrado {cor_pixel} em ({x}, {y}) -> Coordenada corrigida: {coord_escalada}")
                    
                    if not cores_restantes:
                        break
            if not cores_restantes:
                break

        # ... (código para avisar sobre cores não encontradas continua igual) ...

        return coordenadas_encontradas

    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{caminho_imagem}' não encontrado.")
        return None
    except Exception as e:
        print(f"❌ Ocorreu um erro ao processar a imagem: {e}")
        return None

def formatar_dicionario_final(dicionario_coords):
    """Formata o dicionário final com as coordenadas já corrigidas."""
    if not dicionario_coords:
        return

    print("\n" + "="*60)
    print("✅🎉 DICIONÁRIO DE COORDENADAS CORRIGIDO PARA TELA RETINA 🎉✅")
    print("Copie e cole este dicionário no seu script principal do bot.")
    print("="*60 + "\n")
    
    print("PALETA_DE_CORES = {")
    for rgb, pos in dicionario_coords.items():
        print(f"    {rgb}: {pos},")
    print("}")
    print("\n" + "="*60)


if __name__ == "__main__":
    posicoes = encontrar_posicoes_escaladas(CAMINHO_DA_IMAGEM, CORES_PARA_ENCONTRAR, FATOR_ESCALA_RETINA)
    if posicoes:
        formatar_dicionario_final(posicoes)