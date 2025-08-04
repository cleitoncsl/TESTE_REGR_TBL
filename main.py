import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from config.database import SQLServerConnector
from etl.extract_data import carregar_dados
from analysis.explore import analisar_tendencias
from analysis.forecast_banco import prever_crescimento_total

# ✅ novo import
from gerar_arquivos_por_tabela import gerar_arquivos_por_tabela

def testar_conexao():
    try:
        conn = SQLServerConnector().get_connection()
        print("✅ Conexão com o banco SQL Server bem-sucedida.")
        conn.close()
    except Exception as e:
        print("❌ Falha na conexão com o banco:")
        print(e)
        exit(1)

if __name__ == "__main__":
    print("🔌 Testando conexão com o banco de dados...")
    testar_conexao()

    print("📥 Carregando dados da tabela HIST_CRESC_TABELAS...")
    df = carregar_dados()

    print("📊 Realizando análise exploratória...")
    analisar_tendencias(df)

    print("📈 Prevendo crescimento total em registros (RowCounts)...")
    prever_crescimento_total(df, tipo="RowCounts")

    print("💾 Prevendo crescimento total em tamanho (TotalSizeMB)...")
    prever_crescimento_total(df, tipo="TotalSizeMB")

    print("📚 Gerando arquivos individuais por tabela com previsão...")
    gerar_arquivos_por_tabela()

    print("🏁 Finalizado.")
