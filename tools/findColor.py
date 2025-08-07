from PIL import Image
from collections import Counter

# ==================== CONFIGURAÇÃO ====================
# 1. Coloque o nome do seu arquivo de screenshot aqui.
CAMINHO_DA_IMAGEM = 'a.png'  # <-- Use o nome do seu arquivo

# 2. Quantas cores você espera que a paleta tenha?
#    O script vai pegar as cores mais comuns depois do fundo.
NUMERO_DE_CORES_ESPERADO = 63

# 3. A cor de fundo principal da imagem, para ajudar a encontrar a paleta.
COR_DE_FUNDO = (0, 0, 0)
# ======================================================

def encontrar_limites_paleta(img, cor_fundo):
    """Encontra as coordenadas da caixa que contém todos os pixels que não são de fundo."""
    largura, altura = img.size
    min_x, min_y = largura, altura
    max_x, max_y = -1, -1

    for y in range(altura):
        for x in range(largura):
            if img.getpixel((x, y)) != cor_fundo:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    if max_x == -1: # Nenhuma cor diferente do fundo foi encontrada
        return None
        
    # Adiciona uma pequena margem para garantir que pegamos as bordas
    margem = 2 
    return (min_x - margem, min_y - margem, max_x + margem, max_y + margem)

def analisar_paleta_inteligente(caminho_imagem, num_cores_alvo, cor_fundo_geral):
    """
    Analisa uma imagem, corta a paleta de cores e extrai as cores mais frequentes.
    """
    try:
        img = Image.open(caminho_imagem).convert('RGB')
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{caminho_imagem}' não encontrado.")
        return None

    print("1. Encontrando a barra da paleta na imagem...")
    limites = encontrar_limites_paleta(img, cor_fundo_geral)
    if not limites:
        print("❌ Não foi possível encontrar a paleta. A imagem inteira parece ser da cor de fundo.")
        return None
    
    # Corta a imagem para analisar apenas a paleta
    paleta_cortada = img.crop(limites)
    print(f"   Paleta isolada com sucesso!")

    print("\n2. Contando a frequência das cores na paleta...")
    pixels_da_paleta = list(paleta_cortada.getdata())
    contador_cores = Counter(pixels_da_paleta)
    
    # A cor mais comum na paleta cortada é o seu próprio fundo (provavelmente preto ou cinza escuro)
    cores_mais_comuns = contador_cores.most_common(num_cores_alvo + 1) # +1 para incluir o fundo da paleta
    
    print(f"   A cor de fundo da paleta é: {cores_mais_comuns[0][0]} (aparece {cores_mais_comuns[0][1]} vezes)")

    # Extraímos as cores, ignorando a cor de fundo da paleta (o primeiro item da lista)
    cores_finais = [cor for cor, contagem in cores_mais_comuns[1:]]
    
    print(f"\n✅ Análise concluída! Foram extraídas {len(cores_finais)} cores principais.")
    return cores_finais


def formatar_saida(lista_cores):
    """Formata a lista de cores para ser copiada e colada."""
    if not lista_cores:
        return

    print("\n" + "="*55)
    print("🎨 Copie a lista abaixo para a variável 'CORES_PARA_ENCONTRAR'")
    print("   no seu script de calibração ou de limpeza")
    print("="*55 + "\n")
    
    print("CORES_PARA_ENCONTRAR = [")
    for i in range(0, len(lista_cores), 4):
        linha = ", ".join(map(str, lista_cores[i:i+4]))
        print(f"    {linha},")
    print("]")
    print("\n" + "="*55)


if __name__ == "__main__":
    cores_encontradas = analisar_paleta_inteligente(CAMINHO_DA_IMAGEM, NUMERO_DE_CORES_ESPERADO, COR_DE_FUNDO)
    if cores_encontradas:
        formatar_saida(cores_encontradas)