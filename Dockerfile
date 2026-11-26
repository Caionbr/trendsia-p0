# Receita da imagem Docker para rodar a triagem na plataforma Devel (LLM institucional).
# O código é o mesmo da execução local; só a configuração muda (variáveis de ambiente).

# 1. Ponto de partida: um Linux mínimo que já vem com o Python 3.12
FROM python:3.12-slim

# 2. Pasta de trabalho dentro da imagem (equivale a um "cd /app")
WORKDIR /app

# 3. Copia só o que o programa precisa para rodar
COPY requirements.txt pyproject.toml ./
COPY src ./src

# 4. Instala as dependências e o pacote "triagem" (sem guardar cache, para a imagem ficar menor)
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir .

# 5. Valor padrão da espera antes de chamar o LLM, em segundos.
#    A plataforma liga o LLM junto com o container, e ele leva de 1 a 2 minutos para ficar pronto.
ENV ESPERA_LLM=120

# 6. O que roda quando o container é iniciado: espera e depois classifica a mensagem da variável MENSAGEM
CMD ["sh", "-c", "sleep \"$ESPERA_LLM\" && python -m triagem \"$MENSAGEM\""]
