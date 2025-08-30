#!/bin/bash
# This script prepares the environment and runs the main Python application

VENV_DIR=".venv"

echo "--- Verificando o ambiente de execução ---"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Ambiente virtual '$VENV_DIR' não encontrado. Criando um novo..."
    # Create the virtual environment using python3
    python -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar o ambiente virtual. Verifique se 'python3' e o pacote 'venv' estão instalados."
        exit 1
    fi
fi

# Activate the virtual environment
# This line is crucial for isolating the project's dependencies
echo "Ativando o ambiente virtual..."
source "$VENV_DIR/bin/activate"

# Install or update dependencies from requirements.txt
# pip is smart enough to skip packages that are already installed and up-to-date.
echo "Verificando e instalando as dependências do requirements.txt..."
pip install -r requirements.txt

# Now, run the main Python application
echo ""
echo "--- Inicializando o bot ---"
python src/main.py
echo "--- Bot finalizado ---"

# Deactivate the virtual environment upon exiting the script
deactivate
