# Etapa base: imagem leve do Python
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do microserviço para dentro do container
COPY . .

# Expõe a porta que o serviço usa (5001)
EXPOSE 5001

# Comando que inicia o Flask
CMD ["python", "wsgi.py"]
