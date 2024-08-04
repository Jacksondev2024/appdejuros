# Usa a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta em que a aplicação vai rodar
EXPOSE 8080

# Define o comando para rodar a aplicação
CMD ["python", "juros.py"]
