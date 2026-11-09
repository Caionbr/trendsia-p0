# trendsia-p0 — Primeiro fluxo com LLM

Repositório do **projeto P0** da formação [TrendsIA](https://softexcps.org.br/trendsia/), uma formação em Agentes de Inteligência Artificial baseada em projetos (PBL). A formação faz parte do programa TrendsIT, do Núcleo Softex Campinas, com coordenação do Softex e iniciativa do Ministério da Ciência, Tecnologia e Inovação (MCTI).

> **Status:** em desenvolvimento. Este repositório contém, por enquanto, apenas a estrutura inicial.

## Sobre o projeto

O P0 é o primeiro projeto da trilha TrendsIA. O objetivo é construir um **primeiro fluxo funcional com um LLM** (modelo de linguagem de grande porte), servindo de base para os projetos seguintes.

A entrega principal é um **repositório reproduzível em máquina limpa**: qualquer pessoa deve conseguir clonar este repositório, seguir as instruções abaixo e executar o projeto sem depender de configurações do computador do autor.

O desenvolvimento segue os princípios da formação:

- **problema antes de ferramenta**;
- **evidência antes de opinião**;
- **simplicidade antes de complexidade**.


## Estrutura do repositório

```
trendsia-p0/
├── README.md          # este arquivo
├── .env.example       # modelo das variáveis de ambiente (sem segredos)
├── .gitignore         # arquivos que não devem ser versionados
├── requirements.txt   # dependências Python
├── src/               # código-fonte
├── tests/             # casos de teste
├── evidencias/        # registros de execução usados na avaliação
└── docs/
    ├── relatorio.md   # relatório principal do projeto
    └── uso-de-ia.md   # declaração de uso de ferramentas de IA
```

## Requisitos

- Python 3.12 ou superior
- Git
- Acesso a um LLM (o LLM institucional do curso ou outro, registrado em [docs/uso-de-ia.md](docs/uso-de-ia.md))

## Como executar

> As instruções serão completadas conforme o projeto for desenvolvido.

```bash
# 1. Clonar o repositório
git clone https://github.com/Caionbr/trendsia-p0.git
cd trendsia-p0

# 2. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar as variáveis de ambiente
cp .env.example .env
# edite o .env com suas próprias credenciais

# 5. Executar
# (a definir)
```

## Testes

> Os casos de teste ficam em [tests/](tests/). As instruções para executá-los serão adicionadas aqui.

## Níveis de entrega e versões

O projeto é entregue em três níveis. Cada nível é marcado por uma **tag** no repositório:

| Nível | Tag | Status |
|---|---|---|
| Básico | a definir | pendente |
| Intermediário | a definir | pendente |
| Avançado (versão final entregue) | a definir | pendente |

## Documentação

- **Relatório principal:** [docs/relatorio.md](docs/relatorio.md)
- **Uso de IA no desenvolvimento:** [docs/uso-de-ia.md](docs/uso-de-ia.md)
- **Vídeo de apresentação:** (link a definir)

## Autor

- [Caionbr](https://github.com/Caionbr)
