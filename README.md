# WPlace\_Bot

Um bot em Python projetado para automatizar a colocação de pixels em WPlace, funcionando sob circunstâncias muito específicas. Ele opera lendo uma imagem de referência e replicando-a no canvas do jogo, pixel por pixel.

## Funcionalidades

  - **Automatização de Desenho**: Desenha automaticamente uma imagem pré-selecionada no canvas do WPlace.
  - **Calibração Precisa**: Ferramentas para calibrar as coordenadas da paleta de cores e a posição dos botões.
  - **Suporte a Múltiplas Contas**: Capacidade de alternar entre diferentes contas (janelas) para otimizar o tempo de cooldown.
  - **Visualização**: Script para pré-visualizar como a imagem final ficará no jogo.

## Estrutura do Projeto

```
.
├── README.md
├── configs/             # Arquivos de configuração para diferentes imagens
├── images/              # Imagens de referência e seus respectivos redimensionamentos
├── src/                 # Código fonte do bot
│   ├── config.py        # Configurações globais do bot
│   ├── logic.py         # Lógica principal de funcionamento
│   ├── main.py          # Ponto de entrada da aplicação
│   └── utils.py         # Funções utilitárias
└── tools/               # Scripts para tarefas de calibração e preparação
```

## Pré-requisitos

  - Python 3.x
  - Bibliotecas Python (detalhe aqui as bibliotecas necessárias, como `Pillow`, `pyautogui`, etc. Ex: `pip install -r requirements.txt`)
  - [Nome do Jogo/Aplicação] aberto e visível na tela.

-----

## Guia de Instalação e Calibração

Para que o bot funcione corretamente, é necessário passar por um processo de configuração e calibração.

### Passo 1: Preparando a Imagem de Referência

1.  **Escolha sua Imagem**: Selecione a imagem que você deseja desenhar.

2.  **Redimensione a Imagem**: É crucial que a imagem seja redimensionada para que cada "bloco" do jogo corresponda a um pixel. Utilize o script `resize.py` para isso.

      * Coloque sua imagem na pasta `tools`.
      * Execute o comando abaixo, substituindo `<nome>` pelo nome do arquivo e `<proporção>` por um fator de escala (ex: 16). Uma proporção maior deixará a imagem menor.

    <!-- end list -->

    ```bash
    python tools/resize.py <nome_da_imagem.png> <proporção>
    ```

      * O script gerará uma versão `_resized` da sua imagem na mesma pasta. Mova ambas as imagens para uma nova pasta dentro de `images/`.

### Passo 2: Calibrando a Posição das Cores

O bot precisa saber onde clicar para selecionar cada cor.

1.  **Tire um Print da Paleta**: Com o jogo aberto, tire uma print da sua tela completa, mostrando apenas a paleta de cores do jogo. Salve esta imagem como `colors.png` dentro da pasta `tools/`.
2.  **Extrair Posições**:
      * Primeiro, execute `findColor.py` para analisar a imagem e gerar um array das cores.
    <!-- end list -->
    ```bash
    python tools/findColor.py
    ```
      * Copie o array gerado e substitua-o dentro do arquivo `findcolorpallete.py`.
      * Rode `findcolorpallete.py` para obter um objeto Python com as coordenadas de cada cor.
    <!-- end list -->
    ```bash
    python tools/findcolorpallete.py
    ```
3.  **Atualize a Configuração**: Copie o objeto gerado (`PALETA_DE_CORES`) e cole-o no seu arquivo de configuração (veja o Passo 4).

### Passo 3: Calibrando a Posição dos Botões

Você precisa informar ao bot as coordenadas dos elementos da interface. Em sistemas macOS, você pode usar o atalho `Cmd + Shift + 4`, que exibe as coordenadas do cursor na tela, para encontrar as posições necessárias. Em outros sistemas, use ferramentas apropriadas.

### Passo 4: Criando seu Arquivo de Configuração

1.  **Crie um Arquivo**: Vá até a pasta `configs/`, copie o `template.py` e renomeie para um nome de sua escolha (ex: `minha_imagem_config.py`).

2.  **Edite o Arquivo**: Abra seu novo arquivo de configuração e preencha os valores, como a `PALETA_DE_CORES` obtida no passo anterior e as posições dos botões.

3.  **Selecione a Configuração**: Abra o arquivo `src/config.py` e altere a linha 7 para importar seu novo arquivo de configuração. Por exemplo:

    ```python
    # src/config.py
    from configs.minha_imagem_config import *
    ```

-----

## Como Usar o Bot

### 1\. Visualizar o Resultado (Opcional)

Antes de rodar o bot, você pode pré-visualizar como sua imagem ficará no canvas.

1.  Coloque a imagem `_resized.png` na pasta `tools/`.

2.  Execute o script `cV.py`:

    ```bash
    python tools/cV.py <nome_da_imagem_resized.png>
    ```

### 2\. Executando o Bot Principal

Após toda a calibração e configuração:

1.  **Configure Múltiplas Contas (Opcional)**: Se for usar múltiplas contas, abra cada conta em uma janela separada do navegador (guias anônimas ou perfis diferentes). A janela principal (primeira conta) deve estar em tela cheia quando o script for iniciado.

2.  **Ajuste as Configurações Finais**: Verifique as configurações em `src/config.py`, como `NUMERO_DE_CONTAS`, `COOLDOWN_ENTRE_ACOES` e `SWITCH_TABS`.

3.  **Inicie o Script**: Execute o `run.sh` ou diretamente o `main.py`.

    ```bash
    ./run.sh
    # ou
    python src/main.py
    ```

O bot começará a operar, alternando entre as janelas (se configurado) e pintando a imagem no canvas.

-----

### Principais Variáveis de Configuração (`src/config.py`)

| Variável                          | Descrição                                                                              |
| --------------------------------- | -------------------------------------------------------------------------------------- |
| `CAMINHO_SCREENSHOT_TEMP`           | Localização do screenshot temporário da tela do jogo.                                  |
| `PALETA_DE_CORES`                 | Objeto com as coordenadas de cada cor na tela (calibrado anteriormente).               |
| `BOTAO_ABRIR_PALETA_POS`            | Tupla `(x, y)` com a posição do botão para abrir a paleta de cores.                    |
| `COOLDOWN_ENTRE_ACOES`            | Tempo (em segundos) de espera antes de tentar pintar o próximo pixel.                  |
| `ESCALA_TELA`                     | `2` para telas Retina (MacBook), `1` para telas normais.                                 |
| `TOLERANCIA_COR`                  | Margem de diferença para que duas cores sejam consideradas iguais (0-255).             |
| `SWITCH_TABS`                     | `1` para habilitar a troca de contas/janelas, `0` para desabilitar.                    |
| `NUMERO_DE_CONTAS`                | Número de janelas/contas para o bot ciclar.                                            |
| `SLEEP_COEFICIENT`                | Multiplicador para os tempos de espera entre ações, ajustando a velocidade do bot.     |

-----

## Observações

  - Este bot foi criado para um ambiente e resolução de tela específicos. Alterações na resolução ou na interface do jogo exigirão uma nova calibração completa.
  - Use por sua conta e risco. A automação pode violar os termos de serviço de algumas plataformas.