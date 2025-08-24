### README Corrigido e Aprimorado

# WPlace\_Bot

Um bot em Python projetado para automatizar a colocação de pixels em WPlace. Ele opera lendo uma imagem de referência e replicando-a no canvas do jogo, pixel por pixel, de forma otimizada e com suporte a múltiplas contas.

## Funcionalidades

  - **Automatização de Desenho**: Desenha automaticamente uma imagem pré-selecionada no canvas do WPlace.
  - **Detecção Automática de Pixels**: Identifica de forma autônoma a quantidade de pixels disponíveis para uso, sem necessidade de calibração manual.
  - **Suporte a Múltiplas Contas**: Capacidade de alternar entre diferentes janelas para otimizar o tempo de cooldown e acelerar o processo.
  - **Ferramentas de Calibração e Preparação**: Um conjunto de scripts para preparar imagens, extrair paletas de cores e calibrar coordenadas.
  - **Suporte a Telas Retina**: Lógica de correção de coordenadas para funcionar corretamente em telas de alta densidade de pixels (como as de MacBooks).

## Estrutura do Projeto

```
.
├── README.md
├── configs/             # Arquivos de configuração para diferentes artes
├── images/              # Imagens de referência, ícones e capturas de tela
├── src/                 # Código fonte do bot
│   ├── config.py        # Configurações globais e seleção de arte
│   ├── logic.py         # Lógica de comparação de pixels e pintura
│   ├── main.py          # Ponto de entrada da aplicação
│   └── utils.py         # Funções utilitárias (OCR, gerenciamento de contas, etc.)
└── tools/               # Scripts para tarefas de calibração e preparação
```

## Pré-requisitos

  - Python 3.x
  - Tesseract-OCR Engine (instalado no sistema)
  - Bibliotecas Python listadas em `requirements.txt`. Instale-as com:
    ```bash
    pip install -r requirements.txt
    ```
    (As bibliotecas incluem `pyautogui`, `opencv-python`, `pytesseract`, `Pillow`, `playsound` e `numpy`).
  - O jogo/aplicação WPlace aberto e visível na tela.

-----

## Guia de Instalação e Calibração

Para que o bot funcione corretamente, um processo de calibração inicial é necessário.

### Passo 1: Preparando a Imagem de Referência

1.  **Escolha sua Imagem**: Selecione a imagem que deseja desenhar.

2.  **Redimensione a Imagem**: É crucial que a imagem de referência seja redimensionada para que seus pixels correspondam à grade de pixels do canvas do jogo. O script `resize.py` foi projetado para isso.

      * **Objetivo**: Encontrar a `proporção` correta que faz com que a imagem redimensionada tenha exatamente as mesmas dimensões (em pixels) que a área de desenho no jogo.
      * Edite o script `tools/resize.py`, alterando o `input_path` e o `output_path`.
      * Ajuste o valor da variável `proportion`. **Uma proporção maior que 1 aumenta a imagem; menor que 1, diminui.** Você precisará experimentar até que a imagem `_resized.png` gerada tenha o tamanho exato da arte no jogo.
      * Mova a imagem original e a `_resized` para uma nova pasta dentro de `images/paintings/`.

### Passo 2: Calibrando a Posição das Cores

O bot precisa saber onde clicar para selecionar cada cor. Este processo usa dois scripts.

1.  **Tire um Print da Paleta**: Com o jogo aberto, tire um print da tela inteira mostrando a paleta de cores. Salve esta imagem como `a.png` dentro da pasta `tools/`.

2.  **Extraia as Cores**: Execute `findColor.py` para analisar a imagem e gerar uma lista das cores presentes na paleta.

    ```bash
    python tools/findColor.py
    ```

3.  **Encontre as Coordenadas**:

      * Copie a lista de cores gerada no terminal.
      * Abra o script `tools/findcolorpallete.py` e cole a lista na variável `CORES_PARA_ENCONTRAR`.
      * Execute o script para obter um dicionário Python com as coordenadas de cada cor.

    <!-- end list -->

    ```bash
    python tools/findcolorpallete.py
    ```

4.  **Atualize a Configuração**: Copie o dicionário `PALETA_DE_CORES` gerado e cole-o no seu arquivo de configuração de arte (veja o Passo 4).

### Passo 3: Criando seu Arquivo de Configuração de Arte

1.  **Crie um Arquivo**: Na pasta `configs/`, copie o `template.py` e renomeie-o (ex: `minha_arte_config.py`).

2.  **Edite o Arquivo**: Abra seu novo arquivo e preencha **todas as variáveis**, incluindo a `PALETA_DE_CORES` do passo anterior, o `PONTO_DE_ORIGEM_MAPA` (canto superior esquerdo do canvas) e os caminhos para suas imagens.

3.  **Selecione a Configuração**: Abra o arquivo `src/config.py` e altere a importação para usar seu novo arquivo.

    ```python
    # Em src/config.py
    from configs.minha_arte_config import *
    ```

-----

## Como Usar o Bot

### 1\. Pré-visualizar o Resultado (Opcional, mas Recomendado)

Antes de rodar o bot, você pode usar o script `cV.py` (visualizador de cores) para ver como sua imagem `_resized` ficará após ser "quantizada" com a paleta de cores do jogo. Isso ajuda a identificar se as cores da sua imagem correspondem bem às cores disponíveis.

  * Edite o `tools/cV.py` para apontar para seu arquivo de imagem e execute-o.

### 2\. Executando o Bot Principal

Após toda a calibração:

1.  **Configure Múltiplas Contas (Opcional)**: Se for usar, abra cada conta em uma janela separada. A janela da primeira conta deve estar visível e em foco quando o script for iniciado.

2.  **Ajuste as Configurações Finais**: Verifique as variáveis no `src/config.py` (`NUMERO_DE_CONTAS`, `COOLDOWN_ENTRE_ACOES`, `SWITCH_TABS`).

3.  **Inicie o Script**:

    ```bash
    ./run.sh
    # ou
    python src/main.py
    ```

O bot começará a operar após uma contagem regressiva de 10 segundos.

-----

### Principais Variáveis de Configuração

Existem dois níveis de configuração:

#### Variáveis Globais (em `src/config.py`)

| Variável | Descrição |
| :--- | :--- |
| `CAMINHO_IMAGEM_ANCORA` | Caminho para a imagem do ícone (`brush_icon.png`) usado para detectar os pixels disponíveis. |
| `PALETA_DE_CORES` | Dicionário com as coordenadas de cada cor (preenchido pela sua config de arte). |
| `BOTAO_ABRIR_PALETA_POS` | Tupla `(x, y)` com a posição do botão para abrir/fechar a paleta. |
| `COOLDOWN_ENTRE_ACOES` | Tempo (em segundos) de espera entre os ciclos de pintura. |
| `ESCALA_TELA` | `2` para telas Retina (MacBook), `1` para telas normais. |
| `TOLERANCIA_COR` | Margem de diferença para que duas cores no canvas sejam consideradas iguais à do gabarito. |
| `SWITCH_TABS` | `1` para habilitar a troca de contas, `0` para desabilitar. |
| `NUMERO_DE_CONTAS` | Número de janelas/contas para o bot ciclar. |
| `SLEEP_COEFICIENT` | Multiplicador para os `time.sleep`, ajustando a velocidade das ações do mouse. |

#### Variáveis da Arte (em `configs/sua_arte.py`)

| Variável | Descrição |
| :--- | :--- |
| `CAMINHO_IMAGEM_A_PINTAR` | Caminho para a imagem **original** de alta resolução que você quer desenhar. |
| `CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA` | Caminho para a imagem **redimensionada** (`_resized.png`) que serve como gabarito. |
| `PONTO_DE_ORIGEM_MAPA` | **[CRÍTICO]** Tupla `(x, y)` com a coordenada do canto superior esquerdo da área de desenho no jogo. |
| `ESCALA_DE_PIXELS` | Fator de multiplicação dos pixels da imagem redimensionada para a original (geralmente `32`). |

-----

## Observações

  - Este bot foi criado para um ambiente e resolução de tela específicos. Alterações na interface do jogo exigirão uma nova calibração.
  - Use por sua conta e risco. A automação pode violar os termos de serviço de algumas plataformas.