# 📊 HIST_CRESC_ANALISE

Projeto de análise e previsão do crescimento vegetativo de tabelas em um banco de dados SQL Server 2019. Utiliza machine learning (Prophet) para gerar projeções mensais com base em histórico de linhas e tamanho das tabelas.

---

## 🎯 Objetivo

- Realizar o monitoramento contínuo do crescimento das tabelas no banco de dados.
- Gerar previsões mensais com base em dados históricos para planejamento de capacidade.
- Automatizar a conexão com o SQL Server e exportar relatórios em Excel por tabela.

---

## 📂 Estrutura do Projeto

HIST_CRESC_ANALISE/
├── analysis/
│ └── forecast.py # Forecast para o banco completo
│ └── forecast_banco.py # Forecast por tabela
├── config/
│ └── sql_connector.py # Classe de conexão com SQL Server via .env
├── etl/
│ └── load_data.py # Leitura e pré-processamento dos dados
├── data/
│ └── tabelas/ # Arquivos Excel gerados por tabela
├── main.py # Script principal de execução
├── gerar_arquivos_por_tabela.py # Geração de planilhas e previsões por tabela
├── requirements.txt # Lista de dependências
├── .env # Variáveis de ambiente (IGNORADO no Git)
└── .gitignore # Arquivos/pastas ignoradas pelo Git

